const video = document.getElementById("video")
const transcriptDOM = document.getElementById("transcript")
const select = document.getElementById("animeSelect")

let transcript = []
let subtitle = []
let words = []

let lastWord = null
let lastDialog = null

function hasKanji(text){
    return /[\u4e00-\u9faf]/.test(text)
}

/* ================================
   LOAD VIDEO LIST
================================ */

fetch("../video_list.json")
.then(r => r.json())
.then(data => {

    let d = document.createElement("option")
    d.text = "Select Anime"
    d.disabled = true
    d.selected = true
    select.appendChild(d)

    data.videos.forEach(v => {
        let o = document.createElement("option")
        o.value = v
        o.text = v
        select.appendChild(o)
    })
})

/* ================================
   SELECT VIDEO
================================ */

select.addEventListener("change", () => {

    let anime = select.value
    video.src = "../video/" + anime + ".mp4"

    Promise.all([
        fetch("../output/" + anime + "_transcript.json").then(r => r.json()),
        fetch("../output/" + anime + "_subtitle.json").then(r => r.json()),
        fetch("../output/" + anime + "_furigana.json").then(r => r.json())
    ])
    .then(res => {

        transcript = res[0]
        subtitle = res[1]
        words = res[2].words

        renderTranscript()
    })
})

/* ================================
   RENDER TRANSCRIPT (NEW)
================================ */

function renderTranscript(){

    transcriptDOM.innerHTML = ""

    let wordIndex = 0

    transcript.forEach((lineData, i) => {

        let line = document.createElement("div")
        line.className = "dialog"
        line.dataset.start = lineData.start
        line.dataset.end = lineData.end

        let sentence = lineData.text

        // ambil grouping kata dari subtitle (biar ada spasi)
        let sub = subtitle.find(s =>
            s.start <= lineData.start && s.end >= lineData.end
        )

        let tokens = sub ? sub.spaced.split(" ") : sentence.split("")

        tokens.forEach(token => {

            let span = document.createElement("span")
            span.className = "word"

            let w = words[wordIndex]

            if(w){

                if(hasKanji(token) && w.reading){

                    span.innerHTML = `
                        <ruby>
                            ${token}
                            <rt>${w.reading}</rt>
                        </ruby>
                    `

                }else{
                    span.textContent = token
                }

                span.dataset.start = w.start
                span.dataset.end = w.end

                // klik untuk seek
                span.addEventListener("click", () => {
                    video.currentTime = w.start
                })

                wordIndex++

            }else{
                span.textContent = token
            }

            line.appendChild(span)
        })

        transcriptDOM.appendChild(line)
    })
}

/* ================================
   TIME UPDATE (OPTIMIZED)
================================ */

video.addEventListener("timeupdate", () => {

    let t = video.currentTime

    let lines = document.querySelectorAll(".dialog")
    let wordsDOM = document.querySelectorAll(".word")

    /* dialog highlight */
    lines.forEach(line => {

        let s = parseFloat(line.dataset.start)
        let e = parseFloat(line.dataset.end)

        if(t >= s && t <= e){

            if(lastDialog !== line){
                if(lastDialog) lastDialog.classList.remove("active")
                line.classList.add("active")
                line.scrollIntoView({ behavior: "smooth", block: "center" })
                lastDialog = line
            }
        }
    })

    /* word highlight */
    wordsDOM.forEach(w => {

        let s = parseFloat(w.dataset.start)
        let e = parseFloat(w.dataset.end)

        if(!isNaN(s) && !isNaN(e)){

            if(t >= s && t <= e){

                if(lastWord !== w){
                    if(lastWord) lastWord.classList.remove("active-word")
                    w.classList.add("active-word")
                    lastWord = w
                }
            }
        }
    })
})