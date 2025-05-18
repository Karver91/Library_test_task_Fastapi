from fastapi.param_functions import Form
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import EmailStr
from typing_extensions import Annotated, Doc


class CustomOAuth2EmailRequestForm(OAuth2PasswordRequestForm):
    def __init__(
            self,
            username: Annotated[
                EmailStr,
                Form(),
                Doc(
                    """
                    Соответствует спецификации OAuth2 (поля username),
                    но использует валидатор email для входа
                    """
                )
            ],
            password: Annotated[
                str,
                Form(),
                Doc(
                    """
                    `password` string. The OAuth2 spec requires the exact field name
                    `password".
                    """
                ),
            ],
    ):
        super().__init__(username=username, password=password)
