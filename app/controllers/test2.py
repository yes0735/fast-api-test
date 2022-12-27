# -*- coding: utf-8 -*-

from fastapi import APIRouter

from app.common.route import BaseRoute


router = APIRouter(route_class=BaseRoute)
configurations = {
    "swagger": {
        "tags": ["Member API"],
        "tags_metadata": {
            "name": "Member API",
            "description": "계정 관리",
        },
    },
}


@router.get("/member")
async def get_member_list():
    """## Get member List API
    계정 관리 > 계정 리스트 조회
    """

    return {"a2": "aaaaa222"}


@router.get("/member_test")
async def get_member_test():
    """## Get member test API
    계정 관리 > 계정 test 조회
    """

    return {"a2": "aaaaa3333"}
