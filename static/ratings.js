document.addEventListener('DOMContentLoaded', function() {

    let buttons = document.querySelectorAll('.rating-button');

    for (let button of buttons) {

        button.addEventListener('click', async function() {

            let value = Number(this.dataset.value);
            let url = this.dataset.url;

            let response = await fetch(url, {
                method: 'POST',
                headers: {
                    'Content-Type':
                        'application/json;charset=utf-8'
                },
                body: JSON.stringify({
                    value: value
                })
            });

            let data = await response.json();

            if (data.status !== 'ok') {
                return;
            }

            let userRating =
                document.querySelector('#user-rating');

            userRating.textContent =
                'Tvoja ocjena: ' + data.user_rating;

            let averageRating =
                document.querySelector('#average-rating');

            averageRating.textContent =
                'Prosječna ocjena: ' +
                data.average +
                ' (' +
                data.count +
                ' ocjena)';
        });

    }

});