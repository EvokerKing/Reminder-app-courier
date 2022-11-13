import PySimpleGUI as sg
import datetime
from trycourier import Courier
import json
import secrets

client = Courier(auth_token='pk_prod_VKDZ4GDDSEMF4FJ4VZJGD5QV99Y9')


def eventLayout(name: str, time: datetime.datetime, email: str, phone: str) -> list:
    return [name, str(time.date()), str(time.time()), email, phone]


def newReminder(NAME: str, TIME: datetime.datetime, EMAIL: str, PHONE: str) -> None:
    token = secrets.token_hex(16)
    client.profiles.add(
        token,
        {
            "email": EMAIL,
            "phone_number": PHONE
        }
    )
    print(client.automations.invoke_template(
        '12d760b8-debe-40d8-a761-2bc227890fc4',
        data={
            "name": NAME,
            "time": TIME
        },
        profile=token
    ))


with open('items.json', 'r+') as f:
    obj = json.loads(f.read())
layout = [
    [
        sg.Table(
            obj['items'],
            ['Name', 'Date', 'Time', 'Email', 'Phone'],
            auto_size_columns=False,
            col_widths=[25, 10, 10, 35],
            display_row_numbers=True,
            justification='center',
            text_color='white',
            background_color='black',
            alternating_row_color='gray',
            selected_row_colors=('black', 'white'),
            header_text_color='white',
            header_background_color='black',
            vertical_scroll_only=False,
            enable_events=True,
            enable_click_events=True,
            right_click_selects=True,
            expand_x=True,
            expand_y=True,
            key='-TABLE-'
        )
    ],
    [sg.Frame('New Reminder', [
        [sg.Frame('Name', [[sg.Input(key='-NAME-')]])],
        [sg.Frame('Date', [[
            sg.Input(key='-DATE-', size=(10, 1)), sg.CalendarButton('Choose', close_when_date_chosen=False, format='%m/%d/%Y')
        ]]),
            sg.Frame('Time', [[
                sg.DropDown(list(range(1, 25)), key='-HOUR-'), sg.Text(':'), sg.DropDown(list(range(0, 60)), key='-MINUTE-'), sg.Text(':'), sg.DropDown(list(range(0, 60)), key='-SECOND-')
            ]])
        ],
        [],
        [sg.Frame('Notification', [[
            sg.Frame('Email', [[
                sg.Input(key='-EMAIL-')
            ]]),
            sg.Frame('Phone Number', [[
                sg.Input(key='-PHONE-')
            ]])
        ]])],
        [sg.Submit('Submit', key='-SUBMIT-')]
    ])],

]

win = sg.Window('Reminders', layout, resizable=True)

while True:
    event, values = win.read()
    if event == sg.WINDOW_CLOSED:
        break
    elif event == '-SUBMIT-':
        dateinfo = values['-DATE-'].split('/')
        eventlayout = eventLayout(
            values['-NAME-'],
            datetime.datetime(
                int(dateinfo[2]),
                int(dateinfo[0]),
                int(dateinfo[1]),
                int(values['-HOUR-']),
                int(values['-MINUTE-']),
                int(values['-SECOND-'])
            ),
            values['-EMAIL-'],
            values['-PHONE-']
        )
        newReminder(values['-NAME-'], datetime.datetime(int(dateinfo[2]), int(dateinfo[0]), int(dateinfo[1]), int(values['-HOUR-']), int(values['-MINUTE-']), int(values['-SECOND-'])), values['-EMAIL-'], values['-PHONE-'])
        obj['items'].append(eventlayout)
        win['-TABLE-'].update(values=obj['items'])
    else:
        print(event, values)

json.dump(obj, open('items.json', 'w+'))

win.close()
