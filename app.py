import asyncio, aiohttp
from datetime import datetime, timezone
import os, pytz
from threading import Thread
timezone = pytz.timezone('Asia/Tehran')

poke_targets: list = ['https://mercury-broad-meteor.glitch.me/users/records',]
cutoff_level: int = 50
time_to_exit: bool = False
log_file: str = 'logs.fux'
poke_interval: float = 5  # secs

# Todo: Add up/down keyboard action (surfing commands)
# Todo: When adding nonsense websites, other pokes get fucked as well!

def save_targets() -> None:
    targets_file = None
    try:
        targets_file = open('tar.gets', 'w')  # reset log file after 16 mb
        targets_file.write('\n'.join(poke_targets))
        targets_file.close()
    except Exception as ex:
        log("Couldnt save poke targets!", ex)
    finally:
        if targets_file:
            targets_file.close()
def load_targtes() -> list:
    result: list = []
    targets_file = None
    try:
        targets_file = open('tar.gets', 'r')  # reset log file after 16 mb
        result = targets_file.read().split("\n")
        result = list(filter(lambda s: s, result))
    except Exception as ex:
        log("Couldnt load poke targets!", ex)
    finally:
        if targets_file:
            targets_file.close()
    return result

def is_file_size_ok(file_path: str, size_limit_mb: int=16) -> bool:
    # Get file size in bytes
    try:
        file_size_bytes: int = os.path.getsize(file_path)

        # Convert bytes to megabytes
        file_size_mb: int = file_size_bytes // (1024 * 1024)

        # Check if file size is greater than the specified limit
        return file_size_mb <= size_limit_mb  
    except:
        pass
    return True

def log(msg: str, exception: Exception=None) -> None:
    ts = datetime.now(tz=timezone)
    content: str = ts.strftime('%Y-%m-%d %H:%M:%S')
    if exception:
        content = f'{content}\t->\tSHIT: {msg}\n\t\tX: {exception}'
    else:
        content += f'\t->\t{msg}'
    
    logfile = open(log_file, 'a' if is_file_size_ok(log_file) else 'w', encoding='utf-8')  # reset log file after 16 mb
    logfile.write(content + "\n\n")
    logfile.close()

async def poke(url: str):
    async with aiohttp.ClientSession(trust_env=True, ) as session:
        async with session.get(url) as response:
            return await response.text()

async def fuck_around() -> None:
    global cutoff_level, poke_targets
    tasks = [0] * len(poke_targets)
    try:
        for idx, url in enumerate(poke_targets):
            try:
                tasks[idx] = poke(url)
            except Exception as ex:
                log(f'fucked while poking {url}', ex)
        results = await asyncio.gather(*tasks)

        for url, result in zip(poke_targets, results):
            result = result
            log(f"Data from {url}: {result[:cutoff_level] + '...' if cutoff_level < len(result) else result}")
    except Exception as x:
        log(f'well! not i expected', x)
    
async def schedule_pokes() -> None:
    global poke_interval
    while not time_to_exit:
        asyncio.create_task(fuck_around())
        await asyncio.sleep(poke_interval)
        
def full_url(url) -> str:
    return url if 'http://' in url or 'https://' in url else f'https://{url}'

def execute_command(operation, params) -> None:
    global poke_targets, time_to_exit, cutoff_level, poke_interval
    if operation == 'add':
        for url in params:
            url = full_url(url)
            if url not in poke_targets:
                poke_targets.append(url)
                print(f'{url} added to targets.')
            else:
                print(f'{url} already exists in targets.')
        save_targets()
    elif operation == 'del':
        for url in params:
            url = full_url(url)
            if url in poke_targets:
                poke_targets.remove(url)
                print(f'{url} removed.')
            else:
                print(f'no such target as: {url}')
        save_targets()
    elif operation == 'cutoff':
        if len(params) == 1:
            try:
                cf = int(params[0])
                if cf <= 0:
                    raise ValueError()
                cutoff_level = cf
                print(f'cutoff level has been set to {cutoff_level} characters.')
            except ValueError:
                print(f'cutfoff {params[0]} is not valid cause it must be numerical and positive integer!')
        else:
            print('Wrong command! Correct format: cutoff {positive integer}')
            
    elif operation == 'fuckoff':
        time_to_exit = True
        save_targets()
        print('App is scheduled to exit after the next interval...')
    elif operation == 'interval':
        if len(params) == 1:
            try:
                intv = float(params[0])
                if intv <= 0:
                    raise ValueError()
                poke_interval = intv
                print(f'poking interval has been set to {poke_interval} seconds. Applying after next interval.')
            except ValueError:
                print(f'interval {params[0]} is not valid cause it must be a positive floating point number!')
        else:
            print('Wrong command! Correct format: interval {positive number}')
    elif operation == 'help':
        print('''* add domain1 [domain2 domain3 ...]
    Adds and saves the list of domains provided, to the poke list.
    * Note: writing 'http://' or 'https://' is optional. 
* del domain1 [domain2 domain3 ...]
    Deletes them
* interval [number]
    Changes the poking interval to your desired time in seconds. If i remember correctly,
    glith will consider an app as inative, if it doesnt have any api interaction within 5 minutes.
    So set your interval below that, if you want your site to never go to sleep.
    * Note: glitch has another limitation. all your projects can be active nearly 1000 hours a month.
        Consider this in your interval value too.
* cutoff [value]
    cutoff value, is an integer value, which determines how many characters of the get request response, should be logged.
    After that the text will be trunctuated.(...)
* fuckoff
    The app will shutdown after the next interval.
* $ [command index]
    executes previous commands.
    index > 0: execute the (index)th command from all commands, that has been executed so far; starting from the app execution.
    index < 0: execute the latest commands. for example $ -1 will execute previous command.
''')
        
        
def command_line() -> None:
    global time_to_exit
    commands: list = []
    while not time_to_exit:
        cmd = input('> ')
        params = cmd.split()
        operation = params[0].lower()
        if operation == '$':
            try:
                index = int(params[1])
                if index > 0:
                    index -= 1
                print(' '.join(commands[index]))
                operation, params = commands[index][0], commands[index][1:]
                execute_command(operation, params=params)
            except ValueError:
                print(f'cutfoff {params[0]} is not valid cause it must be numerical and positive integer!')
        else:
            execute_command(operation, params=params[1:])
            commands.append(params)
        
async def main() -> None:
    Thread(target=command_line,).start()
    poke_scheduler_task = asyncio.create_task(schedule_pokes())
    await asyncio.gather(poke_scheduler_task)    

    
if __name__ == "__main__":
    targets: list = []
    try:
        targets = load_targtes()
        if targets:
            poke_targets = targets
        asyncio.run(main())
    except Exception as ex:
        log("Program crashed", ex)
    finally:
        if targets:
            save_targets()
