# ISKRobot (일수꾼봇) 이란?
일수꾼봇은 파이썬 및 python-telegram-bot 파이썬 텔레그램 봇 API를 활용하여 만들어진 간단 채무관리 어플리케이션 봇입니다.
친구들끼리 또는 직장 등에서 간단하게 돈을 빌려주었을 때, 채팅을 통해 간단하게 입력해서 관리해 보세요.

모든 텔레그램 봇을 운영하기 위해서는 상시 운영되는 봇 서버가 필요합니다.
본 봇은 테스트 삼아 활용될 수 있는 봇 단계이기에 모두가 사용할 수 있는 샘플 봇은 현재 존재하지 않습니다.
따라서 본 Github의 문서에서는 본인 서버가 존재하는 경우에 운영 방법에 대해서만 설명하고자 합니다.


## 최근 변경사항
version 1.6.1 :
 - [명세] 시, 최근 기록 갯수를 실제 받아온 갯수로 수정하였습니다.

version 1.6.0 :
 - [명세] 뒤에 숫자를 입력하여 조회 건수를 입력할 수 있습니다. (최대 30건)
 - 토큰키를 한 번 입력하면, DB 상에 봇의 토큰키가 자동으로 저장됩니다. 한 번 입력하고 난 뒤에는 입력하지 않아도 됩니다.
 - 기타 소소한 수정이 있었습니다.

version 1.5.2 :
 - [일수] 명령 시, 만약 합계가 0원이 된 경우에는 그 데이터베이스를 삭제합니다.
 - 기타 소소한 소스의 수정이 있었습니다.
 - [조회] / [명세] 에서 버그 해결을 하였습니다. (한 번도 추가 없이 조회할 경우)
 - Docker 쉘 스크립트 등에 수정이 있었습니다.

version 1.5.1 :
 - [더치] 기능을 추가하였습니다. (테스트 기능이라 잘 구현되지 않을 수 있습니다.)
 - (1.5.0에서) 초기화 기능 Inline 구현부를 개발 중입니다. (적용되진 않음)
 - README, Dockerfile 파일 등을 다듬었습니다.

version 1.4.3 :
 - 몇몇 경우에 한해서, 알림소리가 켜지지 않도록 설정하였습니다.

version 1.4.2 :
 - [조회]에서 가장 많은 빚을 소유하고 있는 사람이 위로 나타나게 했습니다.

version 1.4.1 :
 - 계좌 기록의 매끄럽지 못한 부분을 정정합니다.
 - [조회]에서 원이 기록되지 않는 버그를 수정했습니다.

version 1.4  :
 - 데이터베이스로 체계적인 DB 관리를 위해 sqlite3를 활용합니다. SQL문을 활용하여 관리됩니다.
 - 기존에 사용하던 DB는 재사용되지 않습니다. 타 메모장에 기록 후 재활용 부탁드립니다. (공식 테스트 봇은 초기화 될 예정)
 - debt.db 파일에는 본 프로그램의 구동과 관련된 모든 자료가 들어있습니다. 개인정보 보호에 유의해 주십시오.
 - 이제 부분 상환을 위해 사용되던 [부분] 명령어가 사라졌습니다. 모든 입/출금은 [일수] 명령어로 작동합니다.
 - 일수 명령어에서 -(음수)를 사용하면, 부분상환과 같이 작동합니다.
 - 태그 관리의 용이함을 위해, & 태그 대신 # 태그를 활용합니다.
 - 사용 정지를 위한 /stop 프로세스에 변화가 있었습니다. 더 사용이 편리합니다.
 - 데이터 갱신을 위해 Docker 파일의 변동이 있었습니다.


## 라이센스
일수꾼봇은 GPLv3 라이센스를 통해 배포되고 있습니다. 본 프로그램은 그 사실을 명시하는 바이며, 그에 따라 본 봇 소스도 GPL v3 라이센스로 배포하고자 합니다. 자세한 사항은 LICENSE를 참고해 주세요.

python-telegram-bot 모듈은 본 소스 코드에는 포함되어 있지 않으나, lGPLv3 라이센스를 따르고 있습니다.


## 사용을 위해서 필요한 것들
본 봇을 운영하기 위해서는 Python 3 이상을 구동 가능한 PC가 있어야 합니다. 파이썬 3 이상이 설치된 MS Windows, Linux, Unix, Mac OS X 어디든 활용이 가능합니다.

아울러 리눅스 커널의 경우, 유지/관리가 용이하도록 Docker를 빌드해 사용할 수 있습니다. 아래 'Docker를 이용한 봇 사용방법'을 참고해 주세요.


## 이 봇의 활용법
먼저 텔레그램 봇파더(@BotFather)를 통해 봇을 설정하여야 합니다. 봇을 설정한 이후 사용자에게 필요한 값은 TOKEN(토큰) 값입니다.

아울러 pip를 통해 python-telegram-bot 패키지를 설치하여야 합니다. 검색 등을 통하여 관련 글을 읽어보시기 바랍니다. (예: pip install python-telegram-bot)

토큰값을 활용하여, 다음과 같은 명령어 샘플로 실행이 가능합니다.


    python ISKRobot.py <토큰값>

      예) python ISKRobot.py 12345678:A1B2C3D4E5F6G7H8i9_j10k11

    (* 토큰값은 샘플입니다. 이제는 관리자가 각 방별로 /start 명령어를 실행한 사람으로 설정됩니다.)


정상적으로 실행을 하면 "토큰 초기화가 완료되었습니다. 봇을 시작합니다."와 같은 명령어를 만나실 수 있습니다.

토큰 키는 한 번 입력하면 다음부터는 입력하지 않아도 되고, 저장된 토큰키는 새로 입력시 자동으로 업데이트됩니다.

이 봇의 데이터는 봇과의 채팅 및 각 그룹 채팅 모두에서 별도의 데이터로 관리되고 있습니다.

각 방에서 처음으로 /start를 수행한 사람이 추가, 상환 등의 작업이 가능합니다.

모든 기록은 debt.db에 저장되어 관리되고 있습니다. 프로그램을 종료한 이후에도, 다시 실행할 때 그 파일에서 자료를 받아오므로, 활용에 유의하시기 바랍니다.

기존에 사용하시던 debt.dat 및 state.dat는 사용되지 않습니다. 업데이트 이전에 자료를 보존하지 않으면, 지금까지 기록했던 자료들은 사용할 수 없습니다.


## Docker를 이용한 봇 사용방법
리눅스 배포판을 활용하는 경우, 본 봇은 Docker를 통해 이미지 관리가 가능합니다. 본 소스의 Dockerfile은 Docker Hub의 python:3.6-slim을 활용하여 구축되어 있습니다.

핵심적인 ISKRobot.py와 debt.db를 빌드된 Docker 이미지에 저장해 자동으로 실행되도록 활용이 가능합니다.
(단, 데이터 백업은 주석처리 되어 있으므로 필요한 경우에만 활용하기 바람.)

Docker가 설치되어 있는 리눅스 콘솔에서 본 Git 저장소를 다운받은 이후,
(스크립트를 사용하지 않고 Docker의 활용을 위해서는, 아래의 명령어를 수동으로 사용하셔야 합니다.)


    sudo docker build --tag <이미지 태그> .

    sudo docker run --name <프로세스 이름> -d -e TOKENKEY='<토큰값>' -v /etc/localtime:/etc/localtime <이미지 태그>

      예) sudo docker build --tag iskrobot:1.5.2 .

          sudo docker run --name iskrobot-1-5-2 -d -e TOKENKEY='12345678:A1B2C3D4E5F6G7H8i9_j10k11' -v /etc/localtime:/etc/localtime iskrobot:1.5.2

    (* 우분투 배포판 기준. 이미지 태그, 프로세스 이름, 토큰값, 아이디 등은 샘플입니다.)


를 실행해주시면 백그라운드 데몬으로 도커를 실행하실 수 있습니다.

또는 간단하게 bash build_docker.sh 기능을 활용하여 업데이트도 가능합니다. (sh 파일 내용 참조 후 수정하여 사용 요망)


## 명령어 모음
    /start : 처음 봇을 시작하면 만나는 메시지입니다. 각 채팅방에서 봇을 처음 만들때 반드시 입력해 주어야 합니다.

    /help : 각종 명령어에 대한 도움말을 표시하고 있습니다.

    /기타 명령어 : /help를 입력해 확인하실 수 있습니다.


## 기타 자세한 정보
https://blog.gomgom.io/page-about-iskrobot/ 에서 자세하게 다룰 예정입니다.




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