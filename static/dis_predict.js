const input = document.getElementById('symptoms');
const suggestionsBox = document.getElementById('suggestions');

function fetchSuggestions() {
    const value = input.value;
    const terms = value.split(',');
    const currentTerm = terms[terms.length - 1].trim();

    if (currentTerm.length < 1) {
        suggestionsBox.innerHTML = "";
        return;
    }

    const firstChar = currentTerm[0];  // only send first letter to backend
    fetch(`/autocomplete/?letter=${firstChar}`)
        .then(response => response.json())
        .then(data => {
            suggestionsBox.innerHTML = "";
            data.forEach(symptom => {
                const li = document.createElement('li');
                li.textContent = symptom;
                li.style.padding = '5px';
                li.style.cursor = 'pointer';
                li.style.backgroundColor = '#f9f9f9';
                li.style.borderBottom = '1px solid #ddd';

                li.addEventListener('mousedown', () => {
                    terms[terms.length - 1] = symptom;
                    input.value = terms.join(', ') + ', ';
                    suggestionsBox.innerHTML = "";
                });

                suggestionsBox.appendChild(li);
            });
        });
}

input.addEventListener('input', fetchSuggestions);
input.addEventListener('focus', fetchSuggestions);

document.addEventListener('click', (e) => {
    if (!suggestionsBox.contains(e.target) && e.target !== input) {
        suggestionsBox.innerHTML = "";
    }
});
