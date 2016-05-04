"""
 ISKRobot(Il-Su-KKun Robot) (일수꾼봇)

 Created by Gomgom (https://gom2.net)
 Final released: 2016-05-04
 Version: v1.0
"""

import pickle, time, sys
import logging
from telegram.ext import Updater, CommandHandler
from telegram import Emoji

# Checking parameters are or not, if there are, they are put in TOKEN(It's token of this bot) and ADMINID(It's Telegram ID of administrator, if you need)
# Sample exec: python ISKRobot.py 12345678:A1B2C3D4E5F6G7H8i9_j10k11 abcd1234

if len(sys.argv) == 1:
    print("토큰이 입력되지 않았습니다. 매개변수에 TOKEN, 관리자ID 순으로 입력해 주세요.")
    sys.exit()
if len(sys.argv) >= 2:
    TOKEN = str(sys.argv[1])
    if len(sys.argv) == 3:
        ADMINID = sys.argv[2]
        print("관리자가 등록되었습니다. 관리자 이외는 조회 기능만을 이용할 수 있습니다. 관리자는 %s 입니다." % ADMINID)
    elif len(sys.argv) == 2:
        ADMINID = '0'
        print("관리자가 등록되지 않았습니다. 모든 사람이 추가, 상환 등의 이용이 가능합니다.")
    else:
        print("매개변수가 잘못되었습니다. 매개변수에 TOKEN, 관리자ID 순으로 입력해 주세요.")
        sys.exit()

# exec has some information of command and instruction
exec = (("추가", "[이름 금액]\n\t\t\t빚을 추가합니다."), ("조회", "[ ]\n\t\t\t현재 빚 상황을 조회합니다."), ("부분", "[이름 금액]\n\t\t\t부분 상환 금액을 입력합니다."), ("상환", "[이름]\n\t\t\t목록을 삭제합니다."), ("초기화", "[ ]\n\t\t\t모든 빚을 초기화합니다."))
ledger = { }

# Check there is save or not
with open("debt.dat", 'rb') as f:
    ledgerFromFile = pickle.load(f)
    if ledger != ledgerFromFile:
        ledger = ledgerFromFile

# Enable logging
logging.basicConfig(format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s', level = logging.INFO)
logger = logging.getLogger(__name__)

# memoryNow() will perform write time of now in ledger dictionary
def memoryNow():
    ledger['recent'] = time.strftime('%m / %d', time.localtime(time.time()))
    with open("debt.dat", 'wb') as f:
        pickle.dump(ledger, f)

# makeNumToMoney() will perform money will be shown like this (7500000 -> 7,500,000)
def makeNumToMoney(money):
    resNum = ''
    ledgerNum = str(money)
    lessPartNum = len(ledgerNum) % 3
    if len(ledgerNum) > 3:
        if lessPartNum == 0:
            resNum = ledgerNum[:3]
            ledgerNum = ledgerNum[3:]
        else:
            resNum = ledgerNum[:lessPartNum]
            ledgerNum = ledgerNum[lessPartNum:]
        for i in range(0, len(ledgerNum) // 3):
            resNum += "," + ledgerNum[i * 3:(i * 3) + 3]
    else:
        resNum += ledgerNum
    return resNum

# It will show /start
def start(bot, update):
    startMes = '안녕하세요. 저는 일수꾼봇입니다. ' + Emoji.CAT_FACE_WITH_WRY_SMILE + '\n'
    startMes += '여러분들이 빌린 빚을 갚게 하려고 늘 노력하고 있답니다. :)\n'
    startMes += '도움말이 필요하시면 /help를 입력해 주세요. ^^'
    bot.sendMessage(update.message.chat_id, text=startMes)

# It will show /help
def help(bot, update):
    helpMes = '*** 명령어 모음집 *** \n\n'
    for execi in exec:
        helpMes = helpMes + ' - /' + execi[0] + ' ' + execi[1] + '\n'
    helpMes = helpMes + '\n' + ('*' * 19)
    bot.sendMessage(update.message.chat_id, text=helpMes)

# It will be performed when you type, /추가 사람이름 금액
def input(bot, update, args):
    if ADMINID != '0' and update.message.from_user.username != ADMINID:
        return bot.sendMessage(update.message.chat_id, text='내 주인님이 아니에요..-_-+')
    count = 0
    for person in ledger.keys():
        if person == str(args[0]):
            ledger[person] += int(args[1])
            count = 1
            break
    if count == 0:
        ledger[str(args[0])] = int(args[1])
    memoryNow()
    bot.sendMessage(update.message.chat_id, text='추가가 완료되었습니다.')

# It will be performed when you type, /조회
def view(bot, update):
    result = "\n\n" + ("*" * 19) + "\n"
    for person in ledger.keys():
        if person != 'recent':
            result = "  " + result + person + "\t\t\t" + makeNumToMoney(ledger[person]) + "원\n"
    result += "*" * 19
    bot.sendMessage(update.message.chat_id, text='잔금 조회입니다. (' + ledger['recent'] + ' 기준)' + result)

# It will be performed when you type, /부분 사람이름 금액
def returnP(bot, update, args):
    if ADMINID != '0' and update.message.from_user.username != ADMINID:
        return bot.sendMessage(update.message.chat_id, text='내 주인님이 아니에요..-_-+')
    count = 0
    for person in ledger.keys():
        if person == str(args[0]):
            ledger[person] -= int(args[1])
            count = 1
            memoryNow()
            bot.sendMessage(update.message.chat_id, text='부분 상환이 완료되었습니다.')
            break
    if count == 0:
        bot.sendMessage(update.message.chat_id, text='상환할 대상이 없습니다.')

# It will be performed when you type, /상환 사람이름
def remove(bot, update, args):
    if ADMINID != '0' and update.message.from_user.username != ADMINID:
        return bot.sendMessage(update.message.chat_id, text='내 주인님이 아니에요..-_-+')
    count = 0
    for person in ledger.keys():
        if person == str(args[0]):
            del ledger[person]
            count = 1
            memoryNow()
            bot.sendMessage(update.message.chat_id, text='전체 상환이 완료되었습니다.')
            break
    if count == 0:
        bot.sendMessage(update.message.chat_id, text='상환할 대상이 없습니다.')

# It will be performed when you type, /초기화
def reset(bot, update):
    if ADMINID != '0' and update.message.from_user.username != ADMINID:
        return bot.sendMessage(update.message.chat_id, text='내 주인님이 아니에요..-_-+')
    ledger.clear()
    memoryNow()
    bot.sendMessage(update.message.chat_id, text='초기화 작업을 완료했습니다.')

def error(bot, update, error):
    logger.warn('Update "%s" caused error "%s"' % (update, error))

# It is main function of this program
def main():
    updater = Updater(TOKEN)

    dp = updater.dispatcher

    dp.addHandler(CommandHandler("start", start))
    dp.addHandler(CommandHandler("help", help))
    dp.addHandler(CommandHandler(exec[0][0], input, pass_args=True))
    dp.addHandler(CommandHandler(exec[1][0], view))
    dp.addHandler(CommandHandler(exec[2][0], returnP, pass_args=True))
    dp.addHandler(CommandHandler(exec[3][0], remove, pass_args=True))
    dp.addHandler(CommandHandler(exec[4][0], reset))
    dp.addErrorHandler(error)

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()