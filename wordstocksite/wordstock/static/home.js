

async function getArticleLink(link, articleId) {
    await delay(150);
    const article_link = document.getElementById(link)
    let urlInput = document.getElementById("id_url")
    urlInput.value = article_link
    console.log(`${link}, ${articleId}`)
    // createWordcollection(articleId)
}

function clearUrlInput() {
    let urlInput = document.getElementById("id_url")
    urlInput.value = '';
}

function delay(miliseconds) {
    return new Promise(resolve => {
        setTimeout(resolve, miliseconds);
    })
}