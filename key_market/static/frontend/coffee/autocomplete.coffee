do ($=jQuery, window, document) ->

  # AUTOCOMLETE
  # ---------------------------------------------------------------------------
  $ ->
    searchBlock = $ '.search-text'

    escapeRegExChars = (value) ->
      value.replace /[|\\{}()[\]^$+*?.]/g, "\\$&"
      value.split(' ').filter((n) -> n != '').join '|'

    $('#game-search').devbridgeAutocomplete
      serviceUrl: '/api/search_game/'
      paramName: 'title'
      minChars: 2
      maxHeight: 'auto'
      appendTo: searchBlock
      transformResult: (response) ->
        suggestions: $.map JSON.parse(response), (dataItem) ->
          value: dataItem.title, data:
            link: dataItem.url
      formatResult: (suggestion, currentValue) ->
        if not currentValue
          return suggestion.value

        pattern = '(' + escapeRegExChars(currentValue) + ')'
        suggestion.value
          .replace(new RegExp(pattern, 'gi'), '<strong>$1<\/strong>')
          .replace(/&/g, '&amp;')
          .replace(/\s/g, '&nbsp;')
          .replace(/</g, '&lt;')
          .replace(/>/g, '&gt;')
          .replace(/"/g, '&quot;')
          .replace(/&lt;(\/?strong)&gt;/g, '<$1>')

      onSelect: (suggestion) ->
        window.location.href = suggestion.data.link
  # ---------------------------------------------------------------------------
