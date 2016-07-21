"""
 ISKRobot(Il-Su-KKun Robot) (일수꾼봇)

 Created by Gomgom (https://gom2.net)
 Final released: 2016-07-21
 Version: v1.4.0
"""

#
# IMPORT PARTS
#
import sys, os, sqlite3
import logging
from telegram.ext import Updater, CommandHandler
from telegram import Emoji, KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardHide


#
# DEFINE PARTS
#
#
# exec has some information of commands and instructions
exec = (("일수", "[이름 금액 ... #내용]\n\t\t\t빚을 추가/삭제합니다.\n\t\t\t마지막에 '#내용' 추가 가능.\n\
                \t\t\t단, 태그는 띄어쓰기 불가."),
        ("조회", "[ ]\n\t\t\t현재 빚 상황을 조회합니다."),
        ("명세", "[ ]\n\t\t\t최근 기록 내역을 조회합니다."),
        ("상환", "[이름 ...]\n\t\t\t목록을 삭제합니다."),
        ("계좌", "[정보]\n\t\t\t계좌주, 은행, 번호등을 추가합니다."),
        ("초기화", "[ ]\n\t\t\t모든 빚을 초기화합니다."))

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)


#
# FUNCTION PARTS
#
#
# resetdb() will perform make DB if not exists
def resetdb():
    global filelocation
    filelocation = os.path.dirname(__file__) + '/debt.db'
    con = sqlite3.connect(filelocation)
    cur = con.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS t_room (room_id text, owner text, account text, stopchecker int)")
    cur.execute("CREATE TABLE IF NOT EXISTS t_ledger (room_id text, name text, money int)")
    cur.execute("CREATE TABLE IF NOT EXISTS t_state (room_id text, command text, state text, date datetime)")
    con.commit()
    con.close()


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
#
# It will show /start
def start(bot, update):
    # Connect to DB file
    con = sqlite3.connect(filelocation)
    cur = con.cursor()

    startMes = '안녕하세요. 저는 일수꾼봇입니다. ' + Emoji.CAT_FACE_WITH_WRY_SMILE + '\n'
    startMes += '여러분들이 빌린 빚을 갚게 하려고 늘 노력하고 있답니다. :)\n'
    startMes += '도움말이 필요하시면 /help를 입력해 주세요. ^^'

    cur.execute('SELECT COUNT(*) FROM t_room WHERE room_id="' + str(update.message.chat_id) + '"')
    if int(cur.fetchone()[0] == 0):
        cur.execute('INSERT INTO t_room VALUES("' + str(update.message.chat_id) + '", "' + str(update.message.from_user.id) + '", "", 0)')
        con.commit()
        con.close()
        return bot.sendMessage(update.message.chat_id, text=startMes + '\n\n이 방에서 사용이 처음이시네요. 초기화 처리가 완료되었습니다.')
    else:
        con.close()
        return bot.sendMessage(update.message.chat_id, text=startMes + '\n\n이미 이 채팅에는 관리자가 존재합니다.')


# It will show /help
def help(bot, update):
    helpMes = '*** 명령어 모음집 *** \n\n'
    for execi in exec:
        helpMes = helpMes + ' - /' + execi[0] + ' ' + execi[1] + '\n'
    helpMes = helpMes + '\n' + ('*' * 19)

    bot.sendMessage(update.message.chat_id, text=helpMes)


# It will be performed when you type, /일수 사람이름 금액
def input(bot, update, args):
    # Connect to DB file
    con = sqlite3.connect(filelocation)
    cur = con.cursor()

    # Check this chat room is registered, if not, just return
    cur.execute('SELECT COUNT(*) FROM t_room WHERE room_id="' + str(update.message.chat_id) + '"')
    if int(cur.fetchone()[0]) == 0:
        return bot.sendMessage(update.message.chat_id, text='* 이 방에서 초기화가 되지 않았습니다.\n/start를 통해 초기화 후 이용해 주세요. *')
    # Check you're admin or not of this room
    cur.execute('SELECT owner FROM t_room WHERE room_id="' + str(update.message.chat_id) + '"')
    if str(cur.fetchone()[0]) != str(update.message.from_user.id):
        return bot.sendMessage(update.message.chat_id, text='내 주인님이 아니에요..-_-+')

    try:  # For Catching it's number or not
        for i in range(0, (len(args) // 2)):
            int(args[(i*2)+1])  # Change String to Number for checking
        if len(args) % 2 != 0 and str(args[-1])[0:1] != "#":  # Checking final thing is tag or not
            return bot.sendMessage(update.message.chat_id, text='올바르지 않은 입력입니다. /help를 참조해 주세요.')
    except:
        return bot.sendMessage(update.message.chat_id, text='금액에는 숫자만 입력할 수 있습니다.')

    length = len(args)
    if len(args) % 2 == 1 and str(args[:-1])[0:1] == '#':
        length = len(args) - 1

    for i in range(0, length // 2):
        cur.execute('SELECT COUNT(*) FROM t_ledger WHERE room_id="' + str(update.message.chat_id) + '" AND name="' + str(args[i*2]) + '"')
        if int(cur.fetchone()[0]) != 0:
            cur.execute('SELECT money FROM t_ledger WHERE room_id="' + str(update.message.chat_id) + '" AND name="' + str(args[i*2]) + '"')
            curmoney = int(cur.fetchone()[0])
            cur.execute('UPDATE t_ledger SET money=' + str(curmoney + int(args[(i*2)+1])) + ' WHERE room_id="' + str(update.message.chat_id) + '" AND name="' + str(args[i*2]) + '"')
        else:
            cur.execute('INSERT INTO t_ledger VALUES("' + str(update.message.chat_id) + '", "' + str(args[i*2]) + '", "' + str(int(args[(i*2)+1])) + '")')

    cur.execute(
        'INSERT INTO t_state VALUES("' + str(update.message.chat_id) + '", "일수", "' + str(args[0:]) + '", date("now","localtime"))')

    bot.sendMessage(update.message.chat_id, text='추가가 완료되었습니다.')

    con.commit()
    con.close()


# It will be performed when you type, /조회
def view(bot, update):
    # Connect to DB file
    con = sqlite3.connect(filelocation)
    cur = con.cursor()

    # Check this chat room is registered, if not, just return
    cur.execute('SELECT COUNT(*) FROM t_room WHERE room_id="' + str(update.message.chat_id) + '"')
    if int(cur.fetchone()[0]) == 0:
        return bot.sendMessage(update.message.chat_id, text='* 이 방에서 초기화가 되지 않았습니다.\n/start를 통해 초기화 후 이용해 주세요. *')

    cur.execute('SELECT * FROM t_ledger WHERE room_id="' + str(update.message.chat_id) + '" ORDER BY name desc')
    fetchlist = cur.fetchall()

    result = "\n\n" + ("*" * 19) + "\n"
    for i in range(len(fetchlist)):
        result += str(fetchlist[i][1]) + " " + makeNumToMoney((fetchlist[i][2])) + "\n"
    result += "*" * 19

    cur.execute('SELECT account FROM t_room WHERE room_id="' + str(update.message.chat_id) + '"')
    result += "\n[" + str(cur.fetchone()[0]) + "]"

    cur.execute('SELECT * FROM t_state WHERE room_id="' + str(update.message.chat_id) + '" ORDER BY date desc limit 1')
    bot.sendMessage(update.message.chat_id, text='잔금 조회입니다. (' + str(cur.fetchone()[3])[5:] + ' 기준)' + result)
    con.close()


# It will be performed when you type, /명세, it shows your states.
def latest(bot, update):
    # Connect to DB file
    con = sqlite3.connect(filelocation)
    cur = con.cursor()

    # Check this chat room is registered, if not, just return
    cur.execute('SELECT COUNT(*) FROM t_room WHERE room_id="' + str(update.message.chat_id) + '"')
    if int(cur.fetchone()[0]) == 0:
        return bot.sendMessage(update.message.chat_id, text='* 이 방에서 초기화가 되지 않았습니다.\n/start를 통해 초기화 후 이용해 주세요. *')

    # Get latest list of your statements (limit 10)
    cur.execute('SELECT * FROM t_state WHERE room_id="' + str(update.message.chat_id) + '" ORDER BY date desc limit 10')
    fetchlist = cur.fetchall()

    result = "\n\n" + ("#" * 19) + "\n"
    for i in range(len(fetchlist)):
        result += '[' + str(fetchlist[i][1]) + '] '
        for j in range(1, len(fetchlist[i][2])-1):  # For Removing '[', ']'(in loop checker), "'", ','(in loop)
            if str(fetchlist[i][2][j]) == "'" or str(fetchlist[i][2][j]) == ",":
                continue
            else:
                result += str(fetchlist[i][2][j])
        result += '\n'
    result += "#" * 19

    cur.execute('SELECT * FROM t_state WHERE room_id="' + str(update.message.chat_id) + '" ORDER BY date desc limit 1')
    bot.sendMessage(update.message.chat_id, text='최근 명세서입니다. (' + str(cur.fetchone()[3])[5:] + ' 기준)' + result)
    con.close()


# It will be performed when you type, /상환 사람이름
def remove(bot, update, args):
    # Connect to DB file
    con = sqlite3.connect(filelocation)
    cur = con.cursor()

    # Check this chat room is registered, if not, just return
    cur.execute('SELECT COUNT(*) FROM t_room WHERE room_id="' + str(update.message.chat_id) + '"')
    if int(cur.fetchone()[0]) == 0:
        return bot.sendMessage(update.message.chat_id, text='* 이 방에서 초기화가 되지 않았습니다.\n/start를 통해 초기화 후 이용해 주세요. *')
    # Check you're admin or not of this room
    cur.execute('SELECT owner FROM t_room WHERE room_id="' + str(update.message.chat_id) + '"')
    if str(cur.fetchone()[0]) != str(update.message.from_user.id):
        return bot.sendMessage(update.message.chat_id, text='내 주인님이 아니에요..-_-+')

    cur.execute('SELECT name FROM t_ledger WHERE room_id="' + str(update.message.chat_id) + '"')
    fetchlist = cur.fetchall()

    for i in range(len(args)):
        counter = 0
        for j in range(len(fetchlist)):
            if str(fetchlist[j][0]) == str(args[i]):
                cur.execute('DELETE FROM t_ledger WHERE room_id="' + str(update.message.chat_id) + '" AND name="' + str(args[i]) + '"')
                counter = 1
        if counter == 1:
            bot.sendMessage(update.message.chat_id, text='%s(이)에 대한 전체 상환이 완료되었습니다.' % str(args[i]))
        else:
            bot.sendMessage(update.message.chat_id, text='%s은(는) 존재하지 않습니다. 다시 확인해 주세요.' % str(args[i]))

    cur.execute(
        'INSERT INTO t_state VALUES("' + str(update.message.chat_id) + '", "상환", "' + str(args[0:]) + '", date("now","localtime"))')

    con.commit()
    con.close()


# It will be performed when you type, /초기화
def reset(bot, update):
    # Connect to DB file
    con = sqlite3.connect(filelocation)
    cur = con.cursor()

    # Check this chat room is registered, if not, just return
    cur.execute('SELECT COUNT(*) FROM t_room WHERE room_id="' + str(update.message.chat_id) + '"')
    if int(cur.fetchone()[0]) == 0:
        return bot.sendMessage(update.message.chat_id, text='* 이 방에서 초기화가 되지 않았습니다.\n/start를 통해 초기화 후 이용해 주세요. *')
    # Check you're admin or not of this room
    cur.execute('SELECT owner FROM t_room WHERE room_id="' + str(update.message.chat_id) + '"')
    if str(cur.fetchone()[0]) != str(update.message.from_user.id):
        return bot.sendMessage(update.message.chat_id, text='내 주인님이 아니에요..-_-+')

    cur.execute('DELETE FROM t_ledger WHERE room_id="' + str(update.message.chat_id) + '"')

    cur.execute(
        'INSERT INTO t_state VALUES("' + str(update.message.chat_id) + '", "초기화", "' + ' 처리되었습니다.' + '", date("now","localtime"))')

    bot.sendMessage(update.message.chat_id, text='초기화 작업을 완료했습니다.')

    con.commit()
    con.close()


def account(bot, update, args):
    # Connect to DB file
    con = sqlite3.connect(filelocation)
    cur = con.cursor()

    # Check this chat room is registered, if not, just return
    cur.execute('SELECT COUNT(*) FROM t_room WHERE room_id="' + str(update.message.chat_id) + '"')
    if int(cur.fetchone()[0]) == 0:
        return bot.sendMessage(update.message.chat_id, text='* 이 방에서 초기화가 되지 않았습니다.\n/start를 통해 초기화 후 이용해 주세요. *')
    # Check you're admin or not of this room
    cur.execute('SELECT owner FROM t_room WHERE room_id="' + str(update.message.chat_id) + '"')
    if str(cur.fetchone()[0]) != str(update.message.from_user.id):
        return bot.sendMessage(update.message.chat_id, text='내 주인님이 아니에요..-_-+')

    accountdata = ''
    for i in range(0,len(args)):
        accountdata += str(args[i]) + ' '

    cur.execute('UPDATE t_room SET account="' + accountdata + '" WHERE room_id="' + str(update.message.chat_id) + '"')
    bot.sendMessage(update.message.chat_id, text='계좌가 기록되었습니다.')

    con.commit()
    con.close()


def stop(bot, update):
    # Connect to DB file
    con = sqlite3.connect(filelocation)
    cur = con.cursor()

    # Check this chat room is registered, if not, just return
    cur.execute('SELECT COUNT(*) FROM t_room WHERE room_id="' + str(update.message.chat_id) + '"')
    if int(cur.fetchone()[0]) == 0:
        return bot.sendMessage(update.message.chat_id, text='* 이 방에서 초기화가 되지 않았습니다.\n/start를 통해 초기화 후 이용해 주세요. *')
    # Check you're admin or not of this room
    cur.execute('SELECT owner FROM t_room WHERE room_id="' + str(update.message.chat_id) + '"')
    if str(cur.fetchone()[0]) != str(update.message.from_user.id):
        return bot.sendMessage(update.message.chat_id, text='내 주인님이 아니에요..-_-+')

    cur.execute('SELECT stopchecker FROM t_room WHERE room_id="' + str(update.message.chat_id) + '"')

    if int(cur.fetchone()[0]) == 0:
        cur.execute('UPDATE t_room SET stopchecker=1 WHERE room_id="' + str(update.message.chat_id) + '"')
        con.commit()
        custom_keyboard = [[KeyboardButton("/confirm"), KeyboardButton("/cancel") ]]
        reply_markup = ReplyKeyboardMarkup(custom_keyboard, one_time_keyboard='True')
        bot.sendMessage(update.message.chat_id, text='정말로 사용을 정지하시겠습니까?', reply_markup=reply_markup)

    con.close()


def confirm(bot, update):
    # Connect to DB file
    con = sqlite3.connect(filelocation)
    cur = con.cursor()

    cur.execute('SELECT stopchecker, owner FROM t_room WHERE room_id="' + str(update.message.chat_id) + '"')
    fetchlist = cur.fetchone()

    if int(fetchlist[0]) == 1 and str(fetchlist[1]) == str(update.message.from_user.id):
        cur.execute('DELETE FROM t_ledger WHERE room_id="' + str(update.message.chat_id) + '"')
        cur.execute('DELETE FROM t_room WHERE room_id="' + str(update.message.chat_id) + '"')
        con.commit()
        con.close()
        reply_markup = ReplyKeyboardHide()
        return bot.sendMessage(chat_id=update.message.chat_id, text='이용을 중지합니다. 감사합니다.\n재이용은 다시 /start를 입력해 주세요.',
                               reply_markup=reply_markup)


def cancel(bot, update):
    # Connect to DB file
    con = sqlite3.connect(filelocation)
    cur = con.cursor()

    cur.execute('SELECT stopchecker, owner FROM t_room WHERE room_id="' + str(update.message.chat_id) + '"')
    fetchlist = cur.fetchone()

    if int(fetchlist[0]) == 1 and str(fetchlist[1]) == str(update.message.from_user.id):
        cur.execute('UPDATE t_room SET stopchecker=0 WHERE room_id="' + str(update.message.chat_id) + '"')
        con.commit()
        con.close()
        reply_markup = ReplyKeyboardHide()
        return bot.sendMessage(chat_id=update.message.chat_id, text='취소되었습니다.', reply_markup=reply_markup)


def error(bot, update, error):
    logger.warn('Update "%s" caused error "%s"' % (update, error))


#
# MAIN PARTS
#
# It is main function of this program
def main():
    # Checking parameters is or not, if there is, it's put in TOKEN(It's token of this bot))
    # Sample exec: python ISKRobot.py 12345678:A1B2C3D4E5F6G7H8i9_j10k11
    if len(sys.argv) != 2:
        print("토큰이 입력되지 않았습니다. 매개변수에 TOKEN을 입력해 주세요.")
        sys.exit()
    TOKEN = str(sys.argv[1])
    print("토큰 초기화가 완료되었습니다. 봇을 시작합니다.")

    # Reset Databases
    resetdb()

    # Make Telegram bot updater
    updater = Updater(TOKEN)
    dp = updater.dispatcher

    dp.addHandler(CommandHandler("start", start))
    dp.addHandler(CommandHandler("help", help))
    dp.addHandler(CommandHandler(exec[0][0], input, pass_args=True))
    dp.addHandler(CommandHandler(exec[1][0], view))
    dp.addHandler(CommandHandler(exec[2][0], latest))
    dp.addHandler(CommandHandler(exec[3][0], remove, pass_args=True))
    dp.addHandler(CommandHandler(exec[4][0], account, pass_args=True))
    dp.addHandler(CommandHandler(exec[5][0], reset))
    dp.addHandler(CommandHandler("stop", stop))
    dp.addHandler(CommandHandler("confirm", confirm))
    dp.addHandler(CommandHandler("cancel", cancel))
    dp.addErrorHandler(error)

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()