from datetime import datetime



def valider_dates(initial, finish):
    try:
        date_initial = datetime.strptime(initial, '%Y-%m-%d')
        date_finish = datetime.strptime(finish, '%Y-%m-%d')
        
    except ValueError:
        return {'status': False, 'error': 'Incorrect date params'}
    except TypeError:
        return {'status': True, 'filter': False }

    else:        
        return {'status': True, 'filter': True, 'date_initial': date_initial, 'date_finish': date_finish}
        
def format_to_date(date: str):
    return datetime.strptime(date, '%Y-%m-%d')
