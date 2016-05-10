"""
 ISKRobot(Il-Su-KKun Robot) (일수꾼봇)

 Created by Gomgom (https://gom2.net)
 Final released: 2016-05-06
 Version: v1.2 updated
"""

#
# IMPORT PARTS
#
import sys, time, pickle
import logging
from telegram.ext import Updater, CommandHandler
from telegram import Emoji

#
# DEFINE PARTS
#
# exec has some information of command and instruction
exec = (("추가", "[이름 금액] 순서\n\t\t\t빚을 추가합니다.\n\t\t\t마지막에 '-t 내용' 추가로 태그 추가 가능.\n\t\t\t단, 태그는 띄어쓰기 불가."), ("조회", "[ ]\n\t\t\t현재 빚 상황을 조회합니다."), ("명세", "[ ]\n\t\t\t최근 추가/삭제 내역을 조회합니다."),("부분", "[이름 금액] 순서\n\t\t\t부분 상환 금액을 입력합니다."), ("상환", "[이름] 순서\n\t\t\t목록을 삭제합니다."), ("초기화", "[ ]\n\t\t\t모든 빚을 초기화합니다."))
userLedger = { }
userStatement = { }
TOKEN = ''
ADMINID = ''

# Check there is save or not
with open("./debt.dat", 'rb') as f:
    ledgerFromFile = pickle.load(f)
    if userLedger != ledgerFromFile:
        userLedger = ledgerFromFile
with open("./state.dat", 'rb') as f:
    stateFromFile = pickle.load(f)
    if userStatement != stateFromFile:
        userStatement = stateFromFile

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

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

#
# FUNCTION PARTS
#
# memoryNow() will perform write time of now in ledger dictionary
def memoryNow(id):
    ledger = userLedger[id]
    ledger['recent'] = time.strftime('%m / %d', time.localtime(time.time()))
    userLedger[id] = ledger
    with open("./debt.dat", 'wb') as f:
        pickle.dump(userLedger, f)
    with open("./state.dat", 'wb') as f:
        pickle.dump(userStatement, f)

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

#
# BOT HANDLER PARTS
#
# It will show /start
def start(bot, update):
    startMes = '안녕하세요. 저는 일수꾼봇입니다. ' + Emoji.CAT_FACE_WITH_WRY_SMILE + '\n'
    startMes += '여러분들이 빌린 빚을 갚게 하려고 늘 노력하고 있답니다. :)\n'
    startMes += '도움말이 필요하시면 /help를 입력해 주세요. ^^'

    for ownId in userStatement.keys():
        if str(update.message.chat_id) == ownId: return bot.sendMessage(update.message.chat_id, text=startMes)
    userStatement[str(update.message.chat_id)] = []
    for ownId in userLedger.keys():
        if str(update.message.chat_id) == ownId: return bot.sendMessage(update.message.chat_id, text=startMes)
    userLedger[str(update.message.chat_id)] = {}
    memoryNow(str(update.message.chat_id))
    startMes += '\n\n이 채팅/그룹에서는 이용이 처음이시네요. 새로운 ID가 만들어졌습니다.'

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
    if ADMINID != '0' and update.message.from_user.username != ADMINID: return bot.sendMessage(update.message.chat_id, text='내 주인님이 아니에요..-_-+') # Checking you're owner or not
    if len(args) % 2 == 1: return bot.sendMessage(update.message.chat_id, text='올바르지 않은 입력입니다. /help를 참조해 주세요.') # Checking args number
    try: # For Catching it's number or not
        for i in range(0,(len(args) - 2) // 2): int(args[(i*2)+1])
        if (str(args[len(args) - 2]) != "-t"): int(args[len(args) - 1])
    except: return bot.sendMessage(update.message.chat_id, text='금액에는 숫자만 입력할 수 있습니다.')

    ledger = {}
    statement = []
    checkUser = 0
    for ownId in userLedger.keys():
        if str(update.message.chat_id) == ownId:
            ledger = userLedger[ownId]
            if not userStatement[ownId]: userStatement[ownId] = []
            statement = userStatement[ownId]
            checkUser = 1
    if checkUser == 0:
        return bot.sendMessage(update.message.chat_id, text='* 이 방에서 초기화가 되지 않았습니다.\n/start를 통해 초기화 후 이용해 주세요. *')

    length = len(args)

    if str(args[len(args) - 2]) == "-t": length = len(args) - 2
    for i in range(0,length // 2):
        count = 0
        for person in ledger.keys():
            if person == str(args[i*2]):
                ledger[person] += int(args[(i*2)+1])
                count = 1
        if count == 0:
            ledger[str(args[i*2])] = int(args[(i*2)+1])

    state = " " + exec[0][0] + " : "
    if str(args[len(args) - 2]) == "-t": state = state + "(" + str(args[len(args) - 1]) + ") "
    for i in range(0,length):
        state += args[i] + " "
    state += "\n"
    if len(statement) < 10:
        statement.append(state)
    else:
        del statement[0]
        statement.append(state)

    userLedger[str(update.message.chat_id)] = ledger
    userStatement[str(update.message.chat_id)] = statement
    memoryNow(str(update.message.chat_id))
    bot.sendMessage(update.message.chat_id, text='추가가 완료되었습니다.')

# It will be performed when you type, /명세, it shows your states.
def latest(bot, update):
    statement = []
    checkUser = 0
    for ownId in userLedger.keys():
        if str(update.message.chat_id) == ownId:
            if not userStatement[ownId]: userStatement[ownId] = []
            statement = userStatement[ownId]
            checkUser = 1
    if checkUser == 0:
        return bot.sendMessage(update.message.chat_id, text='* 이 방에서 초기화가 되지 않았습니다.\n/start를 통해 초기화 후 이용해 주세요. *')

    result = "\n\n" + ("#" * 19) + "\n"
    for state in statement:
        result += state
    result += "#" * 19
    bot.sendMessage(update.message.chat_id, text='최근 명세서입니다. (' + userLedger[str(update.message.chat_id)]['recent'] + ' 기준)' + result)

# It will be performed when you type, /조회
def view(bot, update):
    ledger = {}
    checkUser = 0
    for ownId in userLedger.keys():
        if str(update.message.chat_id) == ownId:
            ledger = userLedger[ownId]
            checkUser = 1
    if checkUser == 0:
        return bot.sendMessage(update.message.chat_id, text='* 이 방에서 초기화가 되지 않았습니다.\n/start를 통해 초기화 후 이용해 주세요. *')

    result = "\n\n" + ("*" * 19) + "\n"
    for person in ledger.keys():
        if person != 'recent':
            result = "  " + result + person + "\t\t\t" + makeNumToMoney(ledger[person]) + "원\n"
    result += "*" * 19
    bot.sendMessage(update.message.chat_id, text='잔금 조회입니다. (' + ledger['recent'] + ' 기준)' + result)

# It will be performed when you type, /부분 사람이름 금액
def returnP(bot, update, args):
    if ADMINID != '0' and update.message.from_user.username != ADMINID: return bot.sendMessage(update.message.chat_id, text='내 주인님이 아니에요..-_-+') # Checking you're owner or not
    if len(args) % 2 == 1: return bot.sendMessage(update.message.chat_id, text='올바르지 않은 입력입니다. /help를 참조해 주세요.') # Checking args number
    try: # For Catching it's number or not
        for i in range(0,len(args) // 2): int(args[(i*2)+1])
    except: return bot.sendMessage(update.message.chat_id, text='금액에는 숫자만 입력할 수 있습니다.')

    ledger = {}
    statement = []
    checkUser = 0
    for ownId in userLedger.keys():
        if str(update.message.chat_id) == ownId:
            ledger = userLedger[ownId]
            if not userStatement[ownId]: userStatement[ownId] = []
            statement = userStatement[ownId]
            checkUser = 1
    if checkUser == 0:
        return bot.sendMessage(update.message.chat_id, text='* 이 방에서 초기화가 되지 않았습니다.\n/start를 통해 초기화 후 이용해 주세요. *')

    for i in range(0,len(args) // 2):
        count = 0
        for person in ledger.keys():
            if person == str(args[i*2]):
                ledger[person] -= int(args[(i*2)+1])
                count = 1
                bot.sendMessage(update.message.chat_id, text='%s(이)에 대한 부분 상환이 완료되었습니다.' % str(args[i*2]))
        if count == 0:
            bot.sendMessage(update.message.chat_id, text='%s은(는) 존재하지 않습니다. 다시 확인해 주세요.' % str(args[i*2]))

    state = " " + exec[3][0] + "상환 : "
    for i in args:
        state += i + " "
    state += "\n"
    if len(statement) < 10:
        statement.append(state)
    else:
        del statement[0]
        statement.append(state)

    userLedger[str(update.message.chat_id)] = ledger
    userStatement[str(update.message.chat_id)] = statement
    memoryNow(str(update.message.chat_id))

# It will be performed when you type, /상환 사람이름
def remove(bot, update, args):
    if ADMINID != '0' and update.message.from_user.username != ADMINID: return bot.sendMessage(update.message.chat_id, text='내 주인님이 아니에요..-_-+') # Checking you're owner or not

    ledger = {}
    statement = []
    checkUser = 0
    for ownId in userLedger.keys():
        if str(update.message.chat_id) == ownId:
            ledger = userLedger[ownId]
            if not userStatement[ownId]: userStatement[ownId] = []
            statement = userStatement[ownId]
            checkUser = 1
    if checkUser == 0:
        return bot.sendMessage(update.message.chat_id, text='* 이 방에서 초기화가 되지 않았습니다.\n/start를 통해 초기화 후 이용해 주세요. *')

    delList = [] # Trick for remove various person

    for i in range(0,len(args)):
        count = 0
        for person in ledger.keys():
            if person == str(args[i]):
                delList.append(str(args[i]))
                count = 1
                bot.sendMessage(update.message.chat_id, text='%s(이)에 대한 전체 상환이 완료되었습니다.' % str(args[i]))
        if count == 0:
            bot.sendMessage(update.message.chat_id, text='%s은(는) 존재하지 않습니다. 다시 확인해 주세요.' % str(args[i]))
    for person in delList: # also parts of trick
        del ledger[person]

    state = " 전체" + exec[4][0] + " : "
    for i in args:
        state += i + " "
    state += "\n"
    if len(statement) < 10:
        statement.append(state)
    else:
        del statement[0]
        statement.append(state)

    userLedger[str(update.message.chat_id)] = ledger
    userStatement[str(update.message.chat_id)] = statement
    memoryNow(str(update.message.chat_id))

# It will be performed when you type, /초기화
def reset(bot, update):
    if ADMINID != '0' and update.message.from_user.username != ADMINID: return bot.sendMessage(update.message.chat_id, text='내 주인님이 아니에요..-_-+') # Checking you're owner or not

    ledger = {}
    statement = []
    checkUser = 0
    for ownId in userLedger.keys():
        if str(update.message.chat_id) == ownId:
            ledger = userLedger[ownId]
            if not userStatement[ownId]: userStatement[ownId] = []
            statement = userStatement[ownId]
            checkUser = 1
    if checkUser == 0:
        return bot.sendMessage(update.message.chat_id, text='* 이 방에서 초기화가 되지 않았습니다.\n/start를 통해 초기화 후 이용해 주세요. *')

    ledger.clear()

    state = "  ** " + exec[5][0] + " ** \n"
    if len(statement) < 10:
        statement.append(state)
    else:
        del statement[0]
        statement.append(state)

    userLedger[str(update.message.chat_id)] = ledger
    userStatement[str(update.message.chat_id)] = statement
    memoryNow(str(update.message.chat_id))
    bot.sendMessage(update.message.chat_id, text='초기화 작업을 완료했습니다.')

def error(bot, update, error):
    logger.warn('Update "%s" caused error "%s"' % (update, error))

#
# MAIN PARTS
#
# It is main function of this program
def main():
    updater = Updater(TOKEN)
    dp = updater.dispatcher

    dp.addHandler(CommandHandler("start", start))
    dp.addHandler(CommandHandler("help", help))
    dp.addHandler(CommandHandler(exec[0][0], input, pass_args=True))
    dp.addHandler(CommandHandler(exec[1][0], view))
    dp.addHandler(CommandHandler(exec[2][0], latest))
    dp.addHandler(CommandHandler(exec[3][0], returnP, pass_args=True))
    dp.addHandler(CommandHandler(exec[4][0], remove, pass_args=True))
    dp.addHandler(CommandHandler(exec[5][0], reset))
    dp.addErrorHandler(error)

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()