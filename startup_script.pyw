import socket, time

def lock_workstation():
    import ctypes
    ctypes.windll.user32.LockWorkStation()

def unknown_network():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(('8.8.8.8', 80))
    result = s.getsockname()[0]
    s.close()

    print 'Local ip: %s' % result
    return result != '192.168.0.101'

def kill_dynamic_dns_updater():
    terminate_process("DUC40")

def dns_is_updated():
    import urllib2
    time.sleep(10)
    remote_ip = socket.gethostbyname('rafmsou.no-ip.info')
    print 'rafmsou.no-ip.info ip address lookup is -> %s' % remote_ip
    current_ip = urllib2.urlopen('http://ip.42.pl/raw').read()
    print 'current ip is -> %s' % current_ip
    
    if current_ip == remote_ip:
        print 'dns record is updated'
        return True

    return False

def get_process_id( name ):
    import win32pdh
    object = "Process"
    items, instances = win32pdh.EnumObjectItems( None, None, object,
                                                 win32pdh.PERF_DETAIL_WIZARD )
    val = None
    if name in instances :
        hq = win32pdh.OpenQuery()
        hcs = [ ]
        item = "ID Process"
        path = win32pdh.MakeCounterPath( ( None, object, name, None, 0, item ) )
        hcs.append( win32pdh.AddCounter( hq, path ) )
        win32pdh.CollectQueryData( hq )
        time.sleep( 0.01 )
        win32pdh.CollectQueryData( hq )

        for hc in hcs:
            type, val = win32pdh.GetFormattedCounterValue( hc, win32pdh.PDH_FMT_LONG )
            win32pdh.RemoveCounter( hc )
        win32pdh.CloseQuery( hq )
        return val

def terminate_process( name ):
    import win32api, win32con, win32pdh
    pid = 0
    pid = get_process_id(name)
    if pid > 0:
	    handle = win32api.OpenProcess( win32con.PROCESS_TERMINATE, 0, pid )
	    win32api.TerminateProcess( handle, 0 )
	    win32api.CloseHandle( handle )
    
if __name__ == '__main__':

    if unknown_network():
    	print 'locking workStation ...'
    	lock_workstation()

    print 'cheking dns is updated ...'
    while True:
        if dns_is_updated():
            kill_dynamic_dns_updater()
            break
