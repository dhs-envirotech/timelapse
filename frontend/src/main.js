import cron from 'cron-validate';

const apiEndpoint = import.meta.env.DEV ? 'http://127.0.0.1:3000/api' : '/api';

const form = document.querySelector('form'),
    frequency = document.getElementById('frequency'),
    submitButton = document.getElementById('submit');

const FREQUENCIES = {
    '1h': '0 * * * *',
    '2h': '0 */2 * * *',
    '3h': '0 */3 * * *',
    '4h': '0 */4 * * *',
    '5h': '0 */5 * * *',
    '6h': '0 */6 * * *',
    '7h': '0 */7 * * *',
    '8h': '0 */8 * * *',
    '9h': '0 */9 * * *',
    '10h': '0 */10 * * *',
    '11h': '0 */11 * * *',
    '12h': '0 */12 * * *',
};

// Intialize Frequency Options
for (const label of Object.keys(FREQUENCIES)) {
    const option = document.createElement('option');

    option.setAttribute('value', label);
    option.innerText = label;

    option.selected = true;

    frequency.appendChild(option);
};

// frequency.focus();
// frequency.addEventListener('input', () => {
//     const isInvalid = cron(frequency.value.trim()).isError();

//     frequency.setAttribute('aria-invalid', isInvalid);
//     if (isInvalid) {
//         submitButton.setAttribute('disabled', 'true');
//     } else {
//         submitButton.removeAttribute('disabled');
//     }
// });

form.addEventListener('submit', event => {
    event.preventDefault();

    fetch(apiEndpoint + '/settings', {
        mode: 'no-cors',
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            'cron': FREQUENCIES[frequency.value]
        })
    })
        .catch(console.error)
        .then(console.log);
});