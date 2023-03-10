function deleteNote(noteId) {
  fetch('/delete-note', {
    method: 'POST',
    body: JSON.stringify({ noteId: noteId })
  }).then((_res) => {
    window.location.href = '/';
  });
}

function formAutocomplete() {
  var input = document.getElementById('participant_id');
  var suggestionsDiv = document.getElementById('suggestions');
  var query = input.value;

  if (query.length > 0) {
      $.ajax({
          url: '/autocomplete',
          data: {query: query},
          success: function(suggestions) {
              suggestionsDiv.innerHTML = '';
              if (suggestions.length > 0) {
                suggestions.forEach(function(suggestion) {
                    var suggestionNode = document.createElement('DIV');
                    suggestionNode.innerHTML = suggestion;
                    suggestionNode.addEventListener('click', function() {
                        input.value = suggestion;
                        suggestionsDiv.innerHTML = "";
                        suggestionsDiv.style.display = 'none';
                        });
                    suggestionsDiv.appendChild(suggestionNode);
                    suggestionsDiv.style.display = 'block';
                });
            } else {
                suggestionsDiv.style.display = 'none';
            }
          }
      });
  } else {
      suggestionsDiv.innerHTML = '';
      suggestionsDiv.style.display = 'none';
  }
}