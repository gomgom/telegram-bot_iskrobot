# ISKRobot (일수꾼봇) 이란?
일수꾼봇은 파이썬 및 python-telegram-bot 파이썬 텔레그램 봇 API를 활용하여 만들어진 채무관리 어플리케이션입니다.
친구들끼리 간단하게 돈을 빌려주었을 때 채팅을 통해 간단하게 입력해 보세요.

## 라이센스
일수꾼봇은 GPLv3 라이센스를 통해 배포되고 있습니다. 본 프로그램은 그 사실을 명시하는 바이며, 그에 따라 본 봇 소스도 GPL v3 라이센스로 배포하고자 합니다. 자세한 사항은 LICENSE를 참고해 주세요.
python-telegram-bot 모듈은 본 소스 코드에는 포함되어 있지 않으나, lGPLv3 라이센스를 따르고 있습니다.

## 이 봇의 활용법
먼저 텔레그램 봇파더를 통해 봇을 설정하여야 합니다. 봇을 설정한 이후 사용자에게 필요한 값은 TOKEN(토큰) 값입니다.
아울러 관리자를 설정하고 싶으실 때에는 관리자 사용자 ID를 알아야 합니다. 텔레그램 설정에서 아이디 설정 및 변경이 가능합니다.

두 가지 값을 알고 계신다면, 다음과 같은 명령어 샘플로 실행이 가능합니다.
  python ISKRobot.py 12345678:A1B2C3D4E5F6G7H8i9_j10k11(토큰) abcd1234(아이디)
정상적으로 실행을 하면 "관리자가 등록되었습니다. 관리자 이외는 조회 기능만을 이용할 수 있습니다. 관리자는 abcd1234 입니다."와 같은 명령어를 만나실 수 있습니다.

토큰은 필수이지만, 관리자 ID를 설정하지 않으실 수도 있습니다.
그 경우에는 "관리자가 등록되지 않았습니다. 모든 사람이 추가, 상환 등의 이용이 가능합니다."라는 응답이 나오며 실행되며, 모든 사람이 추가, 상환 등의 작업이 가능합니다.

## 명령어 모음
/start : 처음 봇을 시작하면 만나는 메시지입니다.
/help : 각종 명령어에 대한 도움말을 표시하고 있습니다.
/기타 명령어 : /help를 입력해 확인하실 수 있습니다.

## 기타 자세한 정보
https://gom2.net/page-about-iskrobot/ 에서 자세하게 다룰 예정입니다.


# In English (essential parts)

## Usage
This Telegram Bot was made with python-telegram-bot (by python-telegram-bot) on Github.
I strongly inform the above mentions, therefore the sources of the Bot are under the GPL v3 license.
 ** Telegram Python Bot API is under the LGPL v3 licence.

## Appendix 1: GPL v3 License

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.