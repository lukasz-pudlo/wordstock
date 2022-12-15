
function getCookie(name) {
    var cookieValue = null
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';')
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim()
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1))
                break
            }
        }
    }
    return cookieValue
}
var csrftoken = getCookie('csrftoken')


// Set up variables for the page type (i.e. wordcollection, word, etc.).

var wordcollection_id = ''

var word_id = ''

var synonym_id = ''

var pageType = ''

var url = ''

wordcollection_id = JSON.parse(document.getElementById('wordcollection-id').textContent)

pageType = JSON.parse(document.getElementById('page-type').textContent)

if (pageType == 'wordcollection') {
    url = `http://127.0.0.1:8000/rest-api/wordcollection/${wordcollection_id}/words`
}

else if (pageType == 'word') {
    word_id = JSON.parse(document.getElementById('word-id').textContent)
    console.log(word_id)
    url = `http://127.0.0.1:8000/rest-api/wordcollection/${wordcollection_id}/word/${word_id}/synonyms`
}

else if (pageType == 'synonym') {
    word_id = JSON.parse(document.getElementById('word-id').textContent)
    synonym_id = JSON.parse(document.getElementById('synonym-id').textContent)
    console.log(synonym_id)
    url = `http://127.0.0.1:8000/rest-api/wordcollection/${wordcollection_id}/word/${word_id}/synonym/${synonym_id}/examples`
}


var list_snapshot = []

window.addEventListener('load', function()
{
    var xhr = null

    getXmlHttpRequestObject = function()
    {
        if(!xhr)
        {               
            // Create a new XMLHttpRequest object 
            xhr = new XMLHttpRequest()
        }
        return xhr
    }

    updateLiveData = function()
    {
        url = url
        xhr = getXmlHttpRequestObject()
        xhr.onreadystatechange = eventHandler
        // Asynchronous requests.
        xhr.open("GET", url, true)
        // Send the request over the network.
        xhr.send(null)
    }

    updateLiveData()

    function eventHandler()
    {
        // Check response if is ready or not.
        if(xhr.readyState == 4 && xhr.status == 200)
        {
            var listWrapper = document.getElementById('list-wrapper')
            // Set current data.
            var data = JSON.parse(this.responseText)
            var list = data

            if (list.length != list_snapshot.length) {

                console.log(list)
                
                // Compare the list of data in the database with the current list snapshot and only add new elements to the list.
                for (var i = list_snapshot.length; i < list.length; i++) {
                    var source = ''
                    var target = ''

                    if (pageType == 'wordcollection') {
                        source = `<span class="source_word">${list[i].source_word}</span>`
                        target = `<span class="target_word">${list[i].target_word}</span>`
                    }
                    else if (pageType == 'word') {
                        source = `<span class="source_word">${list[i].source_synonym}</span>`
                        target = `<span class="target_word">${list[i].target_synonym}</span>`
                        }
                    else if (pageType == 'synonym') {
                        source = `<span class="source_word">${list[i].source_example}</span>`
                        target = `<span class="target_word">${list[i].target_example}</span>`
                        }
                    var wordDataRow = `
                        <div id="data-row-${list[i].id}" class="wordcollection-detail-row-wrapper flex-wrapper">
                            <div style="flex: 7">
                                <div id="words-row-${list[i].id}" class="wordcollection-detail-column-wrapper flex-wrapper" onclick="editItem(${list[i].id})">
                                    <h6>
                                        ${source}
                                    </h6>
                                    <h6>
                                        ${target}
                                    </h6>
                                </div>
                            </div>

                            <div style="flex:1">
                                <div id="buttons-${list[i].id}" class="btn-group btn-group-justified" role="group" aria-label="edit and delete buttons">
                                    ${(() => {
                                        if (pageType == 'wordcollection') {
                                            return `
                                                <button class="btn btn-sm btn-outline-dark synonyms-link" onclick="location.href='http://127.0.0.1:8000/wordstock/word/${list[i].id}'">Synonyms</button>
                                            `
                                        }
                                        else if (pageType == 'word') {
                                            return `
                                            <button class="btn btn-sm btn-outline-dark synonyms-link" onclick="location.href='http://127.0.0.1:8000/wordstock/synonym/${list[i].id}'">Examples</button>
                                            `
                                        }
                                        else if (pageType == 'synonym') {
                                            return ''
                                        }
                                        })
                                        
                                        ()}
                                    

                                    <button class="btn btn-sm btn-outline-info edit" onclick="editItem(${list[i].id})">Edit</button>
                                    <button class="btn btn-sm btn-outline-dark delete" onclick="deleteItem(${list[i].id})">X</button>
                                    
                                </div>
                            </div>
                            
                        </div>
                    `
                    listWrapper.insertAdjacentHTML('beforeend', wordDataRow)
                }
            }
            list_snapshot = list
        
            // Update the live data every 1 sec.
            
            setTimeout(updateLiveData(), 1000)
            
            
        }
    }
})

function createEntry() {
    console.log('Create entry clicked')
    document.getElementById("add-entry").style.display = "none"
    var listWrapper = document.getElementById('list-wrapper')
    var createEntryForm = `
        <form id="form-wrapper-create-entry" class="wordcollection-detail-row-wrapper flex-wrapper"> 
            <div style="flex: 7">
                <div class="wordcollection-detail-column-wrapper flex-wrapper">
                        <input id="source-entry-form" class="form-control" type="text" name="source-entry-form" placeholder="Entry in German">
                        <input id="target-entry-form" class="form-control" type="text" name="target-entry-form" placeholder="Entry in English">
                </div>
            </div>
            <div style="flex: 1" class="d-flex justify-content-center">
                    <button class="btn btn-sm btn-outline-secondary" type="submit">Save</button>
                    <button class="btn btn-sm btn-outline-dark delete" onclick="removeCreateForm()">X</button>
            </div>  
        </form>
    `
    
    listWrapper.insertAdjacentHTML('beforebegin', createEntryForm)
    submitCreatedEntry()
}

function removeCreateForm() {
    document.getElementById("form-wrapper-create-entry").remove()
    document.getElementById("add-entry").style.display = "block"
}

async function submitCreatedEntry() {
    var form = await document.getElementById(`form-wrapper-create-entry`)

    form.addEventListener('submit', function(e){
        e.preventDefault()
        
        var url = ''

        var source = document.getElementById(`source-entry-form`)
        
        var target = document.getElementById(`target-entry-form`)
        

        if (pageType == 'wordcollection') {
            url = `http://127.0.0.1:8000/rest-api/word-create`

            fetch(url, {
                method:'POST',
                headers:{
                    'Content-type':'application/json',
                    'X-CSRFToken':csrftoken,
                },
                body:JSON.stringify({'source_word': source.value, 'target_word': target.value, 'wordcollection': wordcollection_id})
            }
            ).then(function(response){
                console.log('Entry created')
                form.reset()
            })
        }

        else if (pageType == 'word') {
            url = `http://127.0.0.1:8000/rest-api/synonym-create`

            fetch(url, {
                method:'POST',
                headers:{
                    'Content-type':'application/json',
                    'X-CSRFToken':csrftoken,
                },
                body:JSON.stringify({'source_synonym': source.value, 'target_synonym': target.value, 'word': word_id})
            }
            ).then(function(response){
                console.log('Entry created')
                form.reset()
            })
        }

        else if (pageType == 'synonym') {
            url = `http://127.0.0.1:8000/rest-api/example-create`

            fetch(url, {
                method:'POST',
                headers:{
                    'Content-type':'application/json',
                    'X-CSRFToken':csrftoken,
                },
                body:JSON.stringify({'source_example': source.value, 'target_example': target.value, 'synonym': synonym_id})
            }
            ).then(function(response){
                console.log('Entry created')
                form.reset()
            })
        }

    })
}


function editItem(itemId){
    var dataRow = document.getElementById(`data-row-${itemId}`)
    var wordRow = document.getElementById(`words-row-${itemId}`)
    var buttons = document.getElementById(`buttons-${itemId}`)
    var source = wordRow.childNodes[1].innerText
    var target = wordRow.childNodes[3].innerText
    buttons.innerHTML = ''
    dataRow.innerHTML = ''


    var words_form = `
        <form id="form-wrapper-${itemId}" class="wordcollection-detail-row-wrapper flex-wrapper"> 
            <div style="flex: 7">
                <div class="wordcollection-detail-column-wrapper flex-wrapper">
                        <input id="source-word-form-${itemId}" class="form-control" type="text" name="source-word-form-${itemId}" value="${source}">
                        <input id="target-word-form-${itemId}" class="form-control" type="text" name="target-word-form-${itemId}" value="${target}">
                </div>
            </div>
            <div style="flex: 1" class="d-flex justify-content-center">
                    <button class="btn btn-sm btn-outline-secondary" type="submit">Save</button>
            </div>  
        </form>
    `

    dataRow.insertAdjacentHTML('beforebegin', words_form)
    dataRow.remove()
    submitEditedItem(itemId)
}


async function submitEditedItem(itemId) {
    var form = await document.getElementById(`form-wrapper-${itemId}`)

    form.addEventListener('submit', function(e){
        e.preventDefault()
        
        var url = ''

        var source = document.getElementById(`source-word-form-${itemId}`)
        var target = document.getElementById(`target-word-form-${itemId}`)

        if (pageType == 'wordcollection') {
            url = `http://127.0.0.1:8000/rest-api/wordcollection/${wordcollection_id}/word-update/${itemId}`

            fetch(url, {
                method:'POST',
                headers:{
                    'Content-type':'application/json',
                    'X-CSRFToken':csrftoken,
                },
                body:JSON.stringify({'id': itemId,'source_word': source.value, 'target_word': target.value, 'wordcollection': wordcollection_id})
            }
            ).then(function(response){
                swapElementsAfterEdit(itemId, source.value, target.value)
            })
        }

        else if (pageType == 'word') {
            url = `http://127.0.0.1:8000/rest-api/wordcollection/${wordcollection_id}/word/${word_id}/synonym-update/${itemId}`
            fetch(url, {
                method:'POST',
                headers:{
                    'Content-type':'application/json',
                    'X-CSRFToken':csrftoken,
                },
                body:JSON.stringify({'id': itemId,'source_synonym': source.value, 'target_synonym': target.value, 'word': word_id})
            }
            ).then(function(response){
                swapElementsAfterEdit(itemId, source.value, target.value)
            })
        }

        else if (pageType == 'synonym') {
            url = `http://127.0.0.1:8000/rest-api/wordcollection/${wordcollection_id}/word/${word_id}/synonym/${synonym_id}/example-update/${itemId}`
            console.log(url)
            console.log(source)
            fetch(url, {
                method:'POST',
                headers:{
                    'Content-type':'application/json',
                    'X-CSRFToken':csrftoken,
                },
                body:JSON.stringify({'id': itemId,'source_example': source.value, 'target_example': target.value, 'synonym': synonym_id})
            }
            ).then(function(response){
                swapElementsAfterEdit(itemId, source.value, target.value)
            })
        }

    })
}

async function swapElementsAfterEdit(itemId, source, target) {
    var elementToSwap = await document.getElementById(`form-wrapper-${itemId}`)
            elementToSwap.innerHTML = ''
            var wordsToInsert = `
                <div id="data-row-${itemId}" class="wordcollection-detail-row-wrapper flex-wrapper">
                    <div style="flex: 7">
                        <div id="words-row-${itemId}" class="wordcollection-detail-column-wrapper flex-wrapper" onclick="editItem(${itemId})">
                            <h6>
                                ${source}
                            </h6>
                            <h6>
                                ${target}
                            </h6>
                        </div>
                    </div>

                    <div style="flex:1">
                        <div id="buttons-${itemId}" class="btn-group btn-group-justified" role="group" aria-label="edit and delete buttons">
                            ${(() => {
                                if (pageType == 'wordcollection') {
                                    return `
                                        <button class="btn btn-sm btn-outline-dark synonyms-link" onclick="location.href='http://127.0.0.1:8000/wordstock/word/${itemId}'">Synonyms</button>
                                    `
                                    }
                                else if (pageType == 'word') {
                                    return `
                                    <button class="btn btn-sm btn-outline-dark synonyms-link" onclick="location.href='http://127.0.0.1:8000/wordstock/synonym/${itemId}'">Examples</button>
                                    `
                                }
                                else if (pageType == 'synonym') {
                                    return ''
                                }
                                })
                                
                                ()}
                        
                            <button class="btn btn-sm btn-outline-info edit" onclick="editItem(${itemId})">Edit</button>
                            <button class="btn btn-sm btn-outline-dark delete" onclick="deleteItem(${itemId})">X</button>
                        </div>
                    </div>
                    
                </div>
            `
            elementToSwap.insertAdjacentHTML('beforebegin', wordsToInsert)
            elementToSwap.remove()
}


function deleteItem(itemId){
    if (pageType == 'wordcollection') {
        fetch(`http://127.0.0.1:8000/rest-api/word-delete/${itemId}`, {
            method:'DELETE', 
            headers:{
                'Content-type':'application/json',
                'X-CSRFToken':csrftoken,
            }
        }).then((response) => {
            document.getElementById(`data-row-${itemId}`).remove()
        })
    }

    else if (pageType == 'word') {
        fetch(`http://127.0.0.1:8000/rest-api/synonym-delete/${itemId}`, {
            method:'DELETE', 
            headers:{
                'Content-type':'application/json',
                'X-CSRFToken':csrftoken,
            }
        }).then((response) => {
            document.getElementById(`data-row-${itemId}`).remove()
        })
    }

    else if (pageType == 'synonym') {
        fetch(`http://127.0.0.1:8000/rest-api/example-delete/${itemId}`, {
            method:'DELETE', 
            headers:{
                'Content-type':'application/json',
                'X-CSRFToken':csrftoken,
            }
        }).then((response) => {
            document.getElementById(`data-row-${itemId}`).remove()
        })
    }

}
