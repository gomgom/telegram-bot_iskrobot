"""
 ISKRobot(Il-Su-KKun Robot) (일수꾼봇)

 Created by Gomgom (https://gom2.net)
 Final released: 2016-07-20
 Version: v1.4.0
"""

#
# IMPORT PARTS
#
import sys, time, pickle, os
import logging
from telegram.ext import Updater, CommandHandler
from telegram import Emoji, KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardHide

# Import SQLite3
import sqlite3


#
# DEFINE PARTS
#
# exec has some information of commands and instructions
exec = (("추가", "[이름 금액 ... &내용]\n\t\t\t빚을 추가합니다.\n\t\t\t마지막에 '&내용' 추가 가능.\n\
                \t\t\t단, 태그는 띄어쓰기 불가."),
        ("조회", "[ ]\n\t\t\t현재 빚 상황을 조회합니다."),
        ("명세", "[ ]\n\t\t\t최근 추가/삭제 내역을 조회합니다."),
        ("부분", "[이름 금액 ...]\n\t\t\t부분 상환 금액을 입력합니다."),
        ("상환", "[이름 ...]\n\t\t\t목록을 삭제합니다."),
        ("초기화", "[ ]\n\t\t\t모든 빚을 초기화합니다."),
        ("계좌", "[정보]\n\t\t\t계좌주, 은행, 번호등을 추가합니다."))
userLedger = { }
userStatement = { }
TOKEN = ''

if os.path.isfile('./debt.db'):
    os.remove('./debt.db')
con = sqlite3.connect("debt.db")
cur = con.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS t_room (room_id text, owner text, account text)")
cur.execute("CREATE TABLE IF NOT EXISTS t_ledger (room_id text, name text, money int)")
con.commit()
con.close()

# Checking parameters is or not, if there is, it's put in TOKEN(It's token of this bot))
# Sample exec: python ISKRobot.py 12345678:A1B2C3D4E5F6G7H8i9_j10k11

'''
if len(sys.argv) != 2:
    print("토큰이 입력되지 않았습니다. 매개변수에 TOKEN을 입력해 주세요.")
    sys.exit()
TOKEN = str(sys.argv[1])
print("토큰 초기화가 완료되었습니다. 봇을 시작합니다.")


# Check there is save or not
if os.path.exists("./debt.dat"):
    with open("./debt.dat", 'rb') as f:
        ledgerFromFile = pickle.load(f)
        if userLedger != ledgerFromFile:
            userLedger = ledgerFromFile
if os.path.exists("./state.dat"):
    with open("./state.dat", 'rb') as f:
        stateFromFile = pickle.load(f)
        if userStatement != stateFromFile:
            userStatement = stateFromFile
'''

TOKEN = '232778291:AAFiGkG1eTsgexNoM-PK5-vmdRx8P1nCvms'
print("토큰 초기화가 완료되었습니다. 봇을 시작합니다.")



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
    con = sqlite3.connect("debt.db")
    cur = con.cursor()

    startMes = '안녕하세요. 저는 일수꾼봇입니다. ' + Emoji.CAT_FACE_WITH_WRY_SMILE + '\n'
    startMes += '여러분들이 빌린 빚을 갚게 하려고 늘 노력하고 있답니다. :)\n'
    startMes += '도움말이 필요하시면 /help를 입력해 주세요. ^^'

#    startMes += '\n\n사용을 원하시는 방에서 #일수꾼을 입력해 주세요.'
    cur.execute('INSERT INTO t_room VALUES("' + str(update.message.chat_id) + '", "' + str(update.message.from_user.id) + '", "' + '")')
    con.commit()
    con.close()
    return bot.sendMessage(update.message.chat_id, text=startMes)
#    else:
#        return bot.sendMessage(update.message.chat_id, text=startMes + '\n\n이미 이 채팅에는 관리자가 존재합니다.')

#def callisk(bot, update):


# It will show /help
def help(bot, update):
    helpMes = '*** 명령어 모음집 *** \n\n'
    for execi in exec:
        helpMes = helpMes + ' - /' + execi[0] + ' ' + execi[1] + '\n'
    helpMes = helpMes + '\n' + ('*' * 19)

    bot.sendMessage(update.message.chat_id, text=helpMes)

# It will be performed when you type, /추가 사람이름 금액
def input(bot, update, args):
    con = sqlite3.connect("debt.db")
    cur = con.cursor()

    cur.execute('INSERT INTO t_ledger VALUES("' + str(update.message.chat_id) + '", "' + str(args[0]) + '", "' + str(args[1]) + '")')
    con.commit()
    con.close()

    bot.sendMessage(update.message.chat_id, text='추가가 완료되었습니다.')

'''
#    if len(args) % 2 == 1: return bot.sendMessage(update.message.chat_id, text='올바르지 않은 입력입니다. /help를 참조해 주세요.') # Checking args number
    try: # For Catching it's number or not
        for i in range(0,(len(args) // 2)): int(args[(i*2)+1])
        if len(args) % 2 != 0 and str(args[len(args) - 1])[0:1] != "&": return bot.sendMessage(update.message.chat_id, text='올바르지 않은 입력입니다. /help를 참조해 주세요.') #
    except: return bot.sendMessage(update.message.chat_id, text='금액에는 숫자만 입력할 수 있습니다.')

    # Check this chat room is registered, if not, just return
    ledger = {}
    statement = []
    if str(update.message.chat_id) in userLedger.keys():
        ledger = userLedger[str(update.message.chat_id)]
        statement = userStatement[str(update.message.chat_id)]
    else:
        return bot.sendMessage(update.message.chat_id, text='* 이 방에서 초기화가 되지 않았습니다.\n/start를 통해 초기화 후 이용해 주세요. *')
    # Check she or he is room leader,
    if userLedger[str(update.message.chat_id)].get('ADMINID', 0) != update.message.from_user.id: return bot.sendMessage(update.message.chat_id, text='내 주인님이 아니에요..-_-+')

    length = len(args)
    if len(args) % 2 != 0 and str(args[:-1])[0:1]: length = len(args) - 1
    for i in range(0,length // 2):
        count = 0
        for person in ledger.keys():
            if person == str(args[i*2]):
                ledger[person] += int(args[(i*2)+1])
                count = 1
        if count == 0:
            ledger[str(args[i*2])] = int(args[(i*2)+1])

    state = " " + exec[0][0] + " : "
    if len(args) % 2 != 0 and str(args[:-1])[0:1]: state = state + "(" + str(args[len(args) - 1]) + ") "
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
'''


# It will be performed when you type, /조회
def view(bot, update):
    con = sqlite3.connect("debt.db")
    cur = con.cursor()
    cur.execute('SELECT * FROM t_ledger')
    viewMes = str(cur.fetchone())

    bot.sendMessage(update.message.chat_id, text='잔금 조회입니다. \n' + )
    con.close()



'''
    # Check this chat room is registered, if not, just return
    ledger = {}
    if str(update.message.chat_id) in userLedger.keys():
        ledger = userLedger[str(update.message.chat_id)]
    else:
        return bot.sendMessage(update.message.chat_id, text='* 이 방에서 초기화가 되지 않았습니다.\n/start를 통해 초기화 후 이용해 주세요. *')

    result = "\n\n" + ("*" * 19) + "\n"
    for person in ledger.keys():
        if person != 'recent' and person != 'removeRequest' and person != 'ADMINID' and person != 'ACCOUNT':
            result = "  " + result + person + "\t\t\t" + makeNumToMoney(ledger[person]) + "원\n"
    if ledger.get('ACCOUNT', '0') != '0': result = result + "\n" + ledger['ACCOUNT'] + "\n"
    result += "*" * 19
    bot.sendMessage(update.message.chat_id, text='잔금 조회입니다. (' + ledger['recent'] + ' 기준)' + result)
'''

# It will be performed when you type, /명세, it shows your states.
def latest(bot, update):
    # Check this chat room is registered, if not, just return
    statement = []
    if str(update.message.chat_id) in userStatement.keys():
        statement = userStatement[str(update.message.chat_id)]
    else:
        return bot.sendMessage(update.message.chat_id, text='* 이 방에서 초기화가 되지 않았습니다.\n/start를 통해 초기화 후 이용해 주세요. *')

    result = "\n\n" + ("#" * 19) + "\n"
    for state in statement:
        result += state
    result += "#" * 19
    bot.sendMessage(update.message.chat_id, text='최근 명세서입니다. (' + userLedger[str(update.message.chat_id)]['recent'] + ' 기준)' + result)

# It will be performed when you type, /부분 사람이름 금액
def returnP(bot, update, args):
    if len(args) % 2 == 1: return bot.sendMessage(update.message.chat_id, text='올바르지 않은 입력입니다. /help를 참조해 주세요.') # Checking args number
    try: # For Catching it's number or not
        for i in range(0,len(args) // 2): int(args[(i*2)+1])
    except: return bot.sendMessage(update.message.chat_id, text='금액에는 숫자만 입력할 수 있습니다.')

    # Check this chat room is registered, if not, just return
    ledger = {}
    statement = []
    if str(update.message.chat_id) in userLedger.keys():
        ledger = userLedger[str(update.message.chat_id)]
        statement = userStatement[str(update.message.chat_id)]
    else:
        return bot.sendMessage(update.message.chat_id, text='* 이 방에서 초기화가 되지 않았습니다.\n/start를 통해 초기화 후 이용해 주세요. *')
    # Check she or he is room leader,
    if userLedger[str(update.message.chat_id)].get('ADMINID', 0) != update.message.from_user.id: return bot.sendMessage(update.message.chat_id, text='내 주인님이 아니에요..-_-+')

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
    # Check this chat room is registered, if not, just return
    ledger = {}
    statement = []
    if str(update.message.chat_id) in userLedger.keys():
        ledger = userLedger[str(update.message.chat_id)]
        statement = userStatement[str(update.message.chat_id)]
    else:
        return bot.sendMessage(update.message.chat_id, text='* 이 방에서 초기화가 되지 않았습니다.\n/start를 통해 초기화 후 이용해 주세요. *')
    # Check she or he is room leader,
    if userLedger[str(update.message.chat_id)].get('ADMINID', 0) != update.message.from_user.id: return bot.sendMessage(update.message.chat_id, text='내 주인님이 아니에요..-_-+')

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
    # Check this chat room is registered, if not, just return
    ledger = {}
    statement = []
    if str(update.message.chat_id) in userLedger.keys():
        ledger = userLedger[str(update.message.chat_id)]
        statement = userStatement[str(update.message.chat_id)]
    else:
        return bot.sendMessage(update.message.chat_id, text='* 이 방에서 초기화가 되지 않았습니다.\n/start를 통해 초기화 후 이용해 주세요. *')
    # Check she or he is room leader,
    if userLedger[str(update.message.chat_id)].get('ADMINID', 0) != update.message.from_user.id: return bot.sendMessage(update.message.chat_id, text='내 주인님이 아니에요..-_-+')

    ledger.clear()
    ledger['ADMINID'] = update.message.from_user.id

    state = "  ** " + exec[5][0] + "가 수행됨. ** \n"
    if len(statement) < 10:
        statement.append(state)
    else:
        del statement[0]
        statement.append(state)

    userLedger[str(update.message.chat_id)] = ledger
    userStatement[str(update.message.chat_id)] = statement
    memoryNow(str(update.message.chat_id))
    bot.sendMessage(update.message.chat_id, text='초기화 작업을 완료했습니다.')

def account(bot, update, args):
    # Check this chat room is registered, if not, just return
    ledger = {}
    if str(update.message.chat_id) in userLedger.keys():
        ledger = userLedger[str(update.message.chat_id)]
    else:
        return bot.sendMessage(update.message.chat_id, text='* 이 방에서 초기화가 되지 않았습니다.\n/start를 통해 초기화 후 이용해 주세요. *')
    # Check she or he is room leader,
    if userLedger[str(update.message.chat_id)].get('ADMINID', 0) != update.message.from_user.id: return bot.sendMessage(update.message.chat_id, text='내 주인님이 아니에요..-_-+')

    accountn = ''
    for i in range(0,len(args)):
        accountn += str(args[i]) + ' '
    ledger['ACCOUNT'] = accountn

    userLedger[str(update.message.chat_id)] = ledger
    bot.sendMessage(update.message.chat_id, text='계좌가 기록되었습니다.')

def stop(bot, update):
    # Check this chat room is registered, if not, just return
    if not str(update.message.chat_id) in userLedger.keys():
        return bot.sendMessage(update.message.chat_id, text='* 이 방에서 초기화가 되지 않았습니다.\n/start를 통해 초기화 후 이용해 주세요. *')
    # Check she or he is room leader,
    if userLedger[str(update.message.chat_id)].get('ADMINID', 0) != update.message.from_user.id: return bot.sendMessage(update.message.chat_id, text='내 주인님이 아니에요..-_-+')

    checkUser = 0
    if str(update.message.chat_id) in userLedger.keys():
        if not str(update.message.chat_id) in userStatement.keys(): userStatement[str(update.message.chat_id)] = []
        checkUser = 1
    if checkUser == 0:
        return bot.sendMessage(update.message.chat_id, text='* 이 방에서 초기화가 되지 않았습니다.\n/start를 통해 초기화 후 이용해 주세요. *')

    if userLedger[str(update.message.chat_id)].get('removeRequest', 0) == 0:
        custom_keyboard = [[KeyboardButton("/confirm"), KeyboardButton("/cancel") ]]
        reply_markup = ReplyKeyboardMarkup(custom_keyboard, one_time_keyboard='True')
        bot.sendMessage(chat_id=update.message.from_user.id, text='정말로 초기화하시겠습니까?', reply_markup=reply_markup)
    else:
        return bot.sendMessage(update.message.chat_id, text='일수꾼봇이 개인적으로 보낸 채팅을 확인해주세요.')

    userLedger[str(update.message.chat_id)]['removeRequest'] = str(update.message.from_user.id)

def confirm(bot, update):
    for i in userLedger.keys():
        if userLedger[i].get('removeRequest', '0') == str(update.message.from_user.id):
            del userLedger[i]
            del userStatement[i]
            reply_markup = ReplyKeyboardHide()
            return bot.sendMessage(chat_id=update.message.chat_id, text='이용을 중지합니다. 감사합니다.\n재이용은 이용하실 방에서 /start를 입력해 주세요.', reply_markup=reply_markup)

def cancel(bot, update):
    for i in userLedger.keys():
        if userLedger[i].get('removeRequest', '0') == str(update.message.from_user.id):
            userLedger[i]['removeRequest'] = 0
            reply_markup = ReplyKeyboardHide()
            return bot.sendMessage(chat_id=update.message.chat_id, text='취소되었습니다.', reply_markup=reply_markup)

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
    dp.addHandler(CommandHandler(exec[6][0], account, pass_args=True))
    dp.addHandler(CommandHandler("stop", stop))
    dp.addHandler(CommandHandler("confirm", confirm))
    dp.addHandler(CommandHandler("cancel", cancel))
#    dp.addHandler(CommandHandler("#일수꾼", callisk))
    dp.addErrorHandler(error)

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()