from __future__ import annotations

from aiobotocore.session import get_session


class S3DocumentsService:
    def __init__(
        self,
        *,
        bucket: str,
        region: str,
        access_key_id: str | None,
        secret_access_key: str | None,
        endpoint_url: str | None,
        key_prefix: str = 'legal-docs',
        presigned_ttl_seconds: int = 3600,
    ):
        self._bucket = bucket
        self._region = region or 'us-east-1'
        self._access_key_id = access_key_id
        self._secret_access_key = secret_access_key
        self._endpoint_url = endpoint_url.strip().rstrip('/') if endpoint_url and endpoint_url.strip() else None
        self._key_prefix = key_prefix.strip('/')
        self._presigned_ttl_seconds = presigned_ttl_seconds

    @staticmethod
    def file_name_from_key(key: str) -> str:
        return key.rsplit('/', 1)[-1]

    def build_object_key(self, organization_id: str, document_type: str, file_name: str) -> str:
        safe_name = file_name.replace('/', '_').replace('\\', '_')
        return f'{self._key_prefix}/{organization_id}/{document_type}/{safe_name}'

    def _client_kwargs(self) -> dict[str, object]:
        kw: dict[str, object] = {'region_name': self._region}
        if self._access_key_id:
            kw['aws_access_key_id'] = self._access_key_id
        if self._secret_access_key:
            kw['aws_secret_access_key'] = self._secret_access_key
        if self._endpoint_url:
            kw['endpoint_url'] = self._endpoint_url
        return kw

    async def upload_bytes(self, *, key: str, body: bytes, content_type: str) -> str:
        session = get_session()
        async with session.create_client('s3', **self._client_kwargs()) as client:
            await client.put_object(
                Bucket=self._bucket,
                Key=key,
                Body=body,
                ContentType=content_type,
            )
        return key

    async def generate_presigned_download_url(self, *, key: str, expires_in: int | None = None) -> str:
        ttl = expires_in if expires_in is not None else self._presigned_ttl_seconds
        session = get_session()
        async with session.create_client('s3', **self._client_kwargs()) as client:
            url = await client.generate_presigned_url(
                ClientMethod='get_object',
                Params={'Bucket': self._bucket, 'Key': key},
                ExpiresIn=ttl,
            )
        return url

    async def delete_object(self, *, key: str) -> None:
        session = get_session()
        async with session.create_client('s3', **self._client_kwargs()) as client:
            await client.delete_object(Bucket=self._bucket, Key=key)
