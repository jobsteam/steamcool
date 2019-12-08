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
          value: dataItem.title
          data:
            link: dataItem.url
            img: dataItem.image_url
      formatResult: (suggestion, currentValue) ->
        result = suggestion.value

        if currentValue
          pattern = '(' + escapeRegExChars(currentValue) + ')'
          result = suggestion.value
            .replace(new RegExp(pattern, 'gi'), '<strong>$1<\/strong>')
            .replace(/&/g, '&amp;')
            .replace(/\s/g, '&nbsp;')
            .replace(/</g, '&lt;')
            .replace(/>/g, '&gt;')
            .replace(/"/g, '&quot;')
            .replace(/&lt;(\/?strong)&gt;/g, '<$1>')

        "<div><img src='#{suggestion.data.img}'>#{result}</div>"

      onSelect: (suggestion) ->
        window.location.href = suggestion.data.link
  # ---------------------------------------------------------------------------
