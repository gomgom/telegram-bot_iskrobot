# ISKRobot (일수꾼봇) 이란?
일수꾼봇은 파이썬 및 python-telegram-bot 파이썬 텔레그램 봇 API를 활용하여 만들어진 간단 채무관리 어플리케이션 봇입니다.
친구들끼리 또는 직장 등에서 간단하게 돈을 빌려주었을 때, 채팅을 통해 간단하게 입력해서 관리해 보세요.

모든 텔레그램 봇을 운영하기 위해서는 상시 운영되는 봇 서버가 필요합니다. 본 봇은 테스트 삼아 활용될 수 있는 봇 단계이기에 모두가 사용할 수 있는 샘플 봇은 현재 존재하지 않습니다.
따라서 본 Github의 문서에서는 본인 서버가 존재하는 경우에 운영 방법에 대해서만 설명하고자 합니다.


## 최근 변경사항
version 1.0.1: Dockerfile 추가 및 간단한 소스 수정이 있었습니다.


## 라이센스
일수꾼봇은 GPLv3 라이센스를 통해 배포되고 있습니다. 본 프로그램은 그 사실을 명시하는 바이며, 그에 따라 본 봇 소스도 GPL v3 라이센스로 배포하고자 합니다. 자세한 사항은 LICENSE를 참고해 주세요.
python-telegram-bot 모듈은 본 소스 코드에는 포함되어 있지 않으나, lGPLv3 라이센스를 따르고 있습니다.


## 사용을 위해서 필요한 것들
본 봇을 운영하기 위해서는 Python 3.5.1을 구동 가능한 PC가 있어야 합니다. 파이썬 3.5.1이 설치된 MS Windows, Linux, Unix, Mac OS X 어디든 활용이 가능합니다.
아울러 리눅스 커널의 경우, 유지/관리가 용이하도록 Docker를 빌드해 사용할 수 있습니다. 아래 'Docker를 이용한 봇 사용방법'을 참고해 주세요.


## 이 봇의 활용법
먼저 텔레그램 봇파더(@BotFather)를 통해 봇을 설정하여야 합니다. 봇을 설정한 이후 사용자에게 필요한 값은 TOKEN(토큰) 값입니다.
아울러 관리자를 설정하고 싶으실 때에는 본인 텔레그램 ID 또는 관리자가 될 텔레그램 유저의 사용자 ID 또한 알아야 합니다. 텔레그램 설정에서 아이디 설정 및 변경이 가능합니다.

이 두 가지 값을 알고 계신다면(토큰값만 있어도 사용은 가능합니다.), 다음과 같은 명령어 샘플로 실행이 가능합니다.

  python ISKRobot.py <토큰값> (아이디)
  예) python ISKRobot.py 12345678:A1B2C3D4E5F6G7H8i9_j10k11 abcd1234
    (* 토큰값과 아이디는 샘플입니다. (아이디) 부분은 필요시 생략 가능합니다.)

정상적으로 실행을 하면 "관리자가 등록되었습니다. 관리자 이외는 조회 기능만을 이용할 수 있습니다. 관리자는 abcd1234 입니다."와 같은 명령어를 만나실 수 있습니다.

토큰은 필수이지만, 관리자 ID를 설정하지 않으실 수도 있습니다.
그 경우에는 "관리자가 등록되지 않았습니다. 모든 사람이 추가, 상환 등의 이용이 가능합니다."라는 응답이 나오며 실행되며, 모든 사람이 추가, 상환 등의 작업이 가능합니다.

모든 기록은 debt.dat에 저장되어 관리되고 있습니다. 프로그램을 종료한 이후에도, 다시 실행할 때 그 파일에서 자료를 받아오므로, 활용에 유의하시기 바랍니다.


## Docker를 이용한 봇 사용방법
리눅스 배포판을 활용하는 경우, 본 봇은 Docker를 통해 이미지 관리가 가능합니다. 본 소스의 Dockerfile은 Docker Hub의 Python:3.5.1을 활용하여 구축되어 있습니다.
핵심적인 ISKRobot.py와 debt.dat를 빌드된 Docker 이미지에 저장해 자동으로 실행되도록 활용이 가능합니다.

Docker가 설치되어 있는 리눅스 콘솔에서 본 Git 저장소를 다운받은 이후,

  sudo docker build --tag <이미지 태그> .
  sudo docker run --name <프로세스 이름> -d -e TOKENKEY='<토큰값>' -e ADMINID='(아이디)' -v /etc/localtime:/etc/localtime <이미지 태그>
  예) sudo docker build --tag iskbot:1.0 .
      sudo docker run --name iskbot1-0 -d -e TOKENKEY='12345678:A1B2C3D4E5F6G7H8i9_j10k11' -e ADMINID='abcd1234' -v /etc/localtime:/etc/localtime iskbot:1.0
    (* 우분투 배포판 기준. 이미지 태그, 프로세스 이름, 토큰값, 아이디는 샘플입니다. ADMINID='(아이디)' 부분은 필요시 생략 가능합니다.)

를 실행해주시면 백그라운드 데몬으로 도커를 실행하실 수 있습니다.


## 명령어 모음
/start : 처음 봇을 시작하면 만나는 메시지입니다.
/help : 각종 명령어에 대한 도움말을 표시하고 있습니다.
/기타 명령어 : /help를 입력해 확인하실 수 있습니다.
 * 봇을 그 서버에서 처음 실행한 경우, /조회를 이용할 경우 에러가 발생할 수 있습니다. 반드시 첫 사용시에는 /초기화를 한 이후에 실행하여 주십시오.)


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