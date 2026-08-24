document.addEventListener('DOMContentLoaded', function() {

    let buttons = document.querySelectorAll('.favorite-button');

    for (let button of buttons) {

        button.addEventListener('click', async function() {

            let isFavorite =
                this.dataset.isFavorite === 'true';

            let url;

            if (isFavorite) {
                url = this.dataset.removeUrl;
            }
            else {
                url = this.dataset.addUrl;
            }

            let response = await fetch(url, {
                method: 'POST',
                headers: {
                    'Content-Type':
                        'application/json;charset=utf-8'
                },
                body: JSON.stringify({})
            });

            let data = await response.json();

            if (data.status !== 'ok') {
                return;
            }

            if (data.is_favorite) {
                this.dataset.isFavorite = 'true';
                this.textContent = 'Ukloni iz favorita';
            }
            else {
                this.dataset.isFavorite = 'false';
                this.textContent = 'Dodaj u favorite';

                if (this.dataset.removeCard === 'true') {
                    let card = this.parentNode;
                    card.remove();

                    let cards = document.querySelectorAll(
                        '.favorite-card'
                    );

                    if (cards.length === 0) {
                        let emptyMessage =
                            document.querySelector(
                                '#favorites-empty'
                            );

                        emptyMessage.textContent =
                            'Još nemate spremljenih favorita.';
                    }
                }
            }
        });

    }

});