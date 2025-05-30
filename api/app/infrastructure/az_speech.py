import asyncio
import aiohttp
import re
from collections import defaultdict
from fastapi import HTTPException
from typing import Dict, Any

class AzSpeechClient:
    """Azure Speech Servicesのクライアントクラス"""

    def __init__(self, session: aiohttp.ClientSession, az_speech_key: str, az_speech_endpoint: str):
        self._session = session
        self._endpoint = az_speech_endpoint
        self._headers = self._create_headers(az_speech_key)

    def _create_headers(self, az_speech_key: str) -> Dict[str, str]:
        """HTTPヘッダーを作成する"""
        return {
            "Ocp-Apim-Subscription-Key": az_speech_key,
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Accept-Language": "ja-JP",
            "X-Japan-Force": "True",
        }

    async def close(self) -> None:
        """セッションをクローズする"""
        if not self._session.closed:
            await self._session.close()

    async def create_transcription_job(self, blob_url: str) -> str:
        """文字起こしジョブを作成する"""
        body = self._create_transcription_config(blob_url)
        transcription_url = f"{self._endpoint}/speechtotext/v3.2/transcriptions"
        response_data = await self._post(transcription_url, body)
        return response_data["self"]

    def _create_transcription_config(self, blob_url: str) -> Dict[str, Any]:
        """文字起こし設定を作成する"""
        return {
            "displayName": "Transcription",
            "locale": "ja-JP",
            "contentUrls": [blob_url],
            "properties": {
                "audioLocale": "ja-JP",
                "defaultLanguageCode": "ja-JP",
                "diarizationEnabled": True,
                "punctuationMode": "DictatedAndAutomatic",
                "wordLevelTimestampsEnabled": True,
            },
        }

    async def poll_transcription_status(
        self, 
        job_url: str, 
        max_attempts: int = 240, 
        initial_interval: int = 30
    ) -> str:
        """文字起こしジョブのステータスを確認する"""
        interval = initial_interval
        for _ in range(max_attempts):
            status_data = await self._get(job_url)
            
            if status := status_data["status"]:
                if status == "Succeeded":
                    return status_data["links"]["files"]
                if status in ["Failed", "Cancelled"]:
                    raise HTTPException(500, f"ジョブ失敗: {status}")
            
            await asyncio.sleep(interval)
            interval = min(interval * 2, 60)
        
        raise HTTPException(500, "ジョブのタイムアウト (2時間超過)")

    async def get_transcription_result(self, file_url: str) -> str:
        """文字起こし結果のURLを取得する"""
        file_data = await self._get(file_url)
        return file_data["values"][0]["links"]["contentUrl"]

    async def fetch_transcription_display(self, content_url: str) -> str:
            async with self.session.get(content_url) as response:
                if response.status != 200:
                    raise HTTPException(
                        status_code=response.status,
                        detail=f"contentUrl の取得に失敗しました: {await response.text()}",
                    )
                content_data = await response.json()
                transcription_result = []
                speaker_blocks = defaultdict(list)
                previous_speaker = None
                times = 1

                for i, phrase in enumerate(content_data["recognizedPhrases"]):
                    speaker = phrase.get("speaker", "不明")                
                    nbest = phrase.get("nBest", [])
                    display_text = nbest[0].get("display", "") if nbest else ""  
                    sentences = re.split(r'(?<=[。！？])', display_text)
                    sentences = [s.strip() for s in sentences if s.strip()]
                    if speaker == previous_speaker:
                        speaker_blocks[f"{speaker}-{times}"].extend(sentences)
                        if i == len(content_data["recognizedPhrases"]) - 1:
                            transcription_result.append(f"[speaker {speaker}]\n" + "\n".join(speaker_blocks[f"{speaker}-{times}"]))         
                    else:
                        if previous_speaker is not None:
                            transcription_result.append(f"[speaker {previous_speaker}]\n" + "\n".join(speaker_blocks[f"{previous_speaker}-{times}"]))
                        times += 1
                        speaker_blocks[f"{speaker}-{times}"] = sentences 
                        previous_speaker = speaker
                        if i == len(content_data["recognizedPhrases"]) - 1:
                            transcription_result.append(f"[speaker {speaker}]\n" + "\n".join(speaker_blocks[f"{speaker}-{times}"]))            
                return "\n\n".join(transcription_result)

    async def _get(self, url: str) -> Dict[str, Any]:
        """GETリクエストを実行する"""
        return await self._make_request("GET", url)

    async def _post(self, url: str, json_body: Dict[str, Any]) -> Dict[str, Any]:
        """POSTリクエストを実行する"""
        return await self._make_request("POST", url, json_body)

    async def _make_request(self, method: str, url: str, json_body: Dict[str, Any] = None) -> Dict[str, Any]:
        """HTTPリクエストを実行する"""
        async with self._session.request(method, url, headers=self._headers, json=json_body) as response:
            expected_status = 201 if method == "POST" else 200
            if response.status != expected_status:
                error_msg = "ジョブの作成" if method == "POST" else "リクエスト"
                raise HTTPException(
                    status_code=response.status,
                    detail=f"{error_msg}に失敗しました: {await response.text()}"
                )
            return await response.json()