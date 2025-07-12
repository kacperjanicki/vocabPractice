import { useState } from 'react';
import '../index.css'
import { TiPlus } from "react-icons/ti";

type VocabResult = {
    meaning: string;
    type: string;
    translation: string;
    synonyms: string[];
    examples: string[];
};

const DUMMY_RESULT: VocabResult = {
    translation: "komputer",
    meaning: "Urządzenie elektroniczne do przetwarzania danych.",
    type: "rzeczownik",
    synonyms: ["pecet", "laptop", "maszyna licząca"],
    examples: [
        "Mój komputer jest bardzo szybki.",
        "Kupuję nowy komputer do pracy.",
        "Komputer ułatwia naukę języków."
    ]
};

const VocabEntry = () => {

    const [word, setWord] = useState("");
    const [result, setResult] = useState<VocabResult | null>(null);

    const submitWord = () => {
        /*
            dictionaryapi.dev is responsible for fetching phonetics and other stuff that ai generates
            so we can serve it to the user while ai generating the reponse

            i decided  to use both dictionaryapi.dev and ai, because there's no public api
            that meets my requirements for this project
        */

        // fetch("https://api.dictionaryapi.dev/api/v2/entries/en/" + word)
        //     .then((response) => response.json())
        //     .then((data) => {
        //         console.log(data)
        //     })
        //     .catch((err) => console.error(err));


        fetch("http://localhost:5174/word/" + word)
            .then((response) => response.json())
            .then((data) => {
                console.log(data)
                setResult(data)
            })
            .catch((err) => console.error(err));

        // setResult(DUMMY_RESULT)

        // fetch("http://localhost:5174/word/" + word + "?native=pl?foreign=es")
        //     .then((response) => response.json())
        //     .then((data) => console.log(data.message))
        //     .catch((err) => console.error(err));

    }


    return (
        <>
            <div className="vocabEntry">
                <div className="vocabInputRow">
                    <input
                        type="text"
                        placeholder="Your word..."
                        className="wordInput"
                        onChange={(e) => setWord(e.target.value)}
                        onKeyDown={(e) => e.key === 'Enter' ? submitWord() : ''}
                    />
                    <div className="btnIcon" onClick={submitWord}>
                        <TiPlus size="25px" />
                    </div>
                </div>
                {result && (
                    <div className="vocabResultBox">
                        <div className="vocabResultRow">
                            <span className="vocabLabel">Translation:</span>
                            <span className="vocabValue">{result.translation}</span>
                        </div>
                        <div className="vocabResultRow">
                            <span className="vocabLabel">Meaning:</span>
                            <span className="vocabValue">{result.meaning}</span>
                        </div>
                        <div className="vocabResultRow">
                            <span className="vocabLabel">Type:</span>
                            <span className="vocabValue">{result.type}</span>
                        </div>
                        <div className="vocabResultRow">
                            <span className="vocabLabel">Synonyms:</span>
                            <span className="vocabValue">{result.synonyms.join(', ')}</span>
                        </div>
                        <div className="vocabResultRow">
                            <span className="vocabLabel">Examples:</span>
                            <ul className="vocabExamples">
                                {result.examples.map((ex, idx) => (
                                    <li key={idx}>{ex}</li>
                                ))}
                            </ul>
                        </div>
                    </div>
                )}
            </div>
        </>

    );
}

export default VocabEntry;