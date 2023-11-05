from typing import Annotated

from fastapi import Depends, status, HTTPException

from src.core.redis_config import get_redis
from src.domain.user.user_router import oauth2_scheme


def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    '''
    현재 유저 정보 조회 함수

    인증 token으로 redis 로그인 세션을 조회하여 일치하는 유저의 id를 반환
        Attributes:
                token (str): 현재 로그인되어 있는 access token
            
        Raises:
            HTTP_401_UNAUTHORIZED: token이 redis에 저장되어 있지 않는 경우
        
        Returns:
            user_id (int): 현재 token에 해당하는 유저 ID
    '''
    rd = get_redis()
    user_id = rd.get(token)
    if not user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='로그인이 필요합니다.')
    return int(user_id)