var wordcollection_id = ''

var word_id = ''

var synonym_id = ''

var learnType = JSON.parse(document.getElementById('learn-type').textContent)

switch(learnType) {
    case 'example':
        wordcollection_id = JSON.parse(document.getElementById('wordcollection-id').textContent)
        word_id = JSON.parse(document.getElementById('word-id').textContent)
        synonym_id = JSON.parse(document.getElementById('synonym-id').textContent)

        var learnWrapper = document.getElementById('learn-wrapper')
        var sourceEntry = document.getElementById('source-entry')

        var url = `http://127.0.0.1:8000/rest-api/wordcollection/${wordcollection_id}/word/${word_id}/synonym/${synonym_id}/examples`
        break
    
    case 'synonym':
        wordcollection_id = JSON.parse(document.getElementById('wordcollection-id').textContent)
        word_id = JSON.parse(document.getElementById('word-id').textContent)


        var learnWrapper = document.getElementById('learn-wrapper')
        var sourceEntry = document.getElementById('source-entry')

        var url = `http://127.0.0.1:8000/rest-api/wordcollection/${wordcollection_id}/word/${word_id}/synonyms`
        break

    case 'word':
        wordcollection_id = JSON.parse(document.getElementById('wordcollection-id').textContent)
    
        var learnWrapper = document.getElementById('learn-wrapper')
        var sourceEntry = document.getElementById('source-entry')

        var url = `http://127.0.0.1:8000/rest-api/wordcollection/${wordcollection_id}/words`
        break
}


var list = []


async function getList() {
    var response = await fetch(url)
    
    if (response.ok) {
        var data = await response.json()
        list = data
    }
    
}

getList().then(response => {
    console.log(list)
    var originalLength = list.length
    var listLength = list.length
    var i = 0
    var correctAnswers = 0
    var form = document.getElementById('target-form')
    var inputTranslation = document.getElementById('input-translation')
    var previousButton = document.getElementById('previous')
    var nextButton = document.getElementById('next')
    var score = document.getElementById('score')
    var translationDirection = document.getElementById('translation-direction')
    var translationSource = document.getElementById('translation-source')
    var translationTarget = document.getElementById('translation-target')
    var translationSourceSet = translationSource.innerText

    translationDirection.addEventListener('click', function () {
        var tempTranslationSource = translationSource.innerText
        var tempTranslationTarget = translationTarget.innerText
        translationSource.innerText = tempTranslationTarget
        translationTarget.innerText = tempTranslationSource
        translationSourceSet = translationSource.innerText
        form.reset()
        setSourcesAndTargets()
    })

    function setSourcesAndTargets() {
        console.log('Reset entries clicked')
        switch(true) {
            case (learnType == 'example') && (translationSourceSet == 'German'):
                sourceEntry.innerHTML = list[i].source_example
                break
            case (learnType == 'example') && (translationSourceSet == 'English'):
                sourceEntry.innerHTML = list[i].target_example
                break
            case (learnType == 'synonym') && (translationSourceSet == 'German'):
                sourceEntry.innerHTML = list[i].source_synonym
                break
            case (learnType == 'synonym') && (translationSourceSet == 'English'):
                sourceEntry.innerHTML = list[i].target_synonym
                break
            case (learnType == 'word') && (translationSourceSet == 'German'):
                sourceEntry.innerHTML = list[i].source_word
                break
            case (learnType == 'word') && (translationSourceSet == 'English'):
                sourceEntry.innerHTML = list[i].target_word
                break
        }
    }

    previousButton.addEventListener('click', function() {
        if (i > 0) {
            i -= 1
            console.log(i)
        }
        setSourcesAndTargets()
    })

    nextButton.addEventListener('click', function() {
        console.log('next clicked')
        console.log(i)
        if (i < list.length - 1) {
            i += 1
            
            console.log(i)
        }
        setSourcesAndTargets()
    })
    setSourcesAndTargets()

    form.addEventListener('submit', function(e){
        e.preventDefault()
        console.log(inputTranslation.value)

        var target = ''
        switch(true) {
            case (learnType == 'example') && (translationSourceSet == 'German'):
                target = list[i].target_example
                break
            case (learnType == 'example') && (translationSourceSet == 'English'):
                target = list[i].source_example
                break
            case (learnType == 'synonym') && (translationSourceSet == 'German'):
                target = list[i].target_synonym
                break
            case (learnType == 'synonym') && (translationSourceSet == 'English'):
                target = list[i].source_synonym
                break
            case (learnType == 'word') && (translationSourceSet == 'German'):
                target = list[i].target_word
                break
            case (learnType == 'word') && (translationSourceSet == 'English'):
                target = list[i].source_word
                break
        }
        
        console.log(stringSimilarity.compareTwoStrings(inputTranslation.value, target))

        if (stringSimilarity.compareTwoStrings(inputTranslation.value, target) > 0.5) {
            console.log('Correct translation')

            
            if (correctAnswers < originalLength) {
                form.reset()
                correctAnswers += 1
                score.innerHTML = `${correctAnswers}/${originalLength} correct answers`
                
                list.splice(i, 1)
                listLength = list.length
                if (correctAnswers < originalLength) {
                    if (i == listLength) {  
                        i -= 1
                        setSourcesAndTargets()
                    }
                    else if (i == 0) {
                        setSourcesAndTargets()
                    }
                    else {
                        setSourcesAndTargets()
                    }
                }
                // If the number of correct answers corresponds to the count of the original list of items, it means that the user has completed
                // the session, so the element displaying div and form can be removed. 
                else {
                    sourceEntry.remove()
                    form.remove()
                }
            }
        }
        else {
            form.reset()
            score.innerHTML = 'Incorrect translation'
            score.style.color = 'red'
            setTimeout(function () {
                score.innerHTML = `${correctAnswers}/${originalLength} correct answers`
                score.style.color = 'black'
            }, 3000)
        }
    })


}).catch(error => {
    console.log(`Error: ${error}`)
})

