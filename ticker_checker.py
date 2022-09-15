from datetime import datetime
from json import loads
from time import sleep

from requests import get, put


def main():
    # curl 'https://www.reservasparquesnacionales.es/real/ParquesNac/usu/html/inicio-reserva-oapn.aspx?cen=2&act=+1' \
    #   -H 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9' \
    #   -H 'Accept-Language: en-GB,en-US;q=0.9,en;q=0.8' \
    #   -H 'Cache-Control: max-age=0' \
    #   -H 'Connection: keep-alive' \
    #   -H 'Content-Type: application/x-www-form-urlencoded' \
    #   -H 'Cookie: ASP.NET_SessionId=fqrkarsgyxd11ft41e2nyoc4' \
    #   -H 'Origin: https://www.reservasparquesnacionales.es' \
    #   -H 'Referer: https://www.reservasparquesnacionales.es/real/ParquesNac/usu/html/inicio-reserva-oapn.aspx?cen=2&act=+1' \
    #   -H 'Sec-Fetch-Dest: document' \
    #   -H 'Sec-Fetch-Mode: navigate' \
    #   -H 'Sec-Fetch-Site: same-origin' \
    #   -H 'Sec-Fetch-User: ?1' \
    #   -H 'Upgrade-Insecure-Requests: 1' \
    #   -H 'User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36' \
    #   -H 'sec-ch-ua: "Google Chrome";v="105", "Not)A;Brand";v="8", "Chromium";v="105"' \
    #   -H 'sec-ch-ua-mobile: ?0' \
    #   -H 'sec-ch-ua-platform: "Linux"'

    headers = {
        'accept': 'application/json',
        'x-api-key': 'caminomasca',
    }

    target_date = datetime(year=2022, month=9, day=19)

    while True:
        print('Checking ticket availability...')
        response = get(
            'https://api.volcanoteide.com/products/1927/availability/2022-09',
            headers=headers)
        availability = loads(response.content)
        days = filter(
            lambda x: datetime.fromisoformat(x['date']) > target_date,
            availability.get('availability', []))

        if not days:
            print('No tickets for this month available!')

        for day in days:
            sessions = day.get('sessions', [])
            is_availabe = False

            for session in sessions:
                is_availabe = session.get('available', 0) > 0

                if is_availabe:
                    put('https://ntfy.sh/teneryfa_masca', json=day)
                    print('Sent notification!')
                    break

            if is_availabe:
                break

        print('Sleeping...')
        sleep(60)


if __name__ == '__main__':
    main()
