import { useState } from 'react';
import '../index.css'
import { TiPlus } from "react-icons/ti";
import type { Country } from '../types/Country';

type VocabResult = {
    translation: string;
    meaning: string;
    examples: string[];
    synonyms: string[];
    type: string;
};

const DUMMY_RESULT: VocabResult = {
    translation: "-",
    meaning: "-",
    type: "-",
    synonyms: ["-", "-", "-"],
    examples: [
        "-",
        "-",
        "-"
    ]
};

type VocabEntryProps = {
    nativeLanguage: Country | null;
    foreignLanguage: Country | null;
};


const VocabEntry = ({ nativeLanguage, foreignLanguage }: VocabEntryProps) => {
    const [word, setWord] = useState("");
    const [result, setResult] = useState<VocabResult | null>();
    const [loading, setLoading] = useState(false);

    const submitWord = () => {
        setLoading(true)
        setResult(DUMMY_RESULT)

        console.log("native: " + nativeLanguage?.code +
            "\nforeign: " + foreignLanguage?.code
        );



        /*
            libretranslate is responsible for fetching simple translation and phonetics,
            so we can serve it to the user while ai is generating the full response

            i decided  to use both libretranslate and ai, because there's no public api
            that meets my requirements for this project
        */

        // const res = await fetch("http://localhost:5000/translate", {
        //     method: "POST",
        //     body: JSON.stringify({
        //         q: word,
        //         source: "en",
        //         target: "pl",
        //         format: "text",
        //         alternatives: 3,
        //         api_key: ""
        //     }),
        //     headers: { "Content-Type": "application/json" }
        // });
        // console.log(await res.json());

        fetch(
            "http://localhost:5174/word/" + word
            + "?native=" + nativeLanguage?.code + "&foreign=" + foreignLanguage?.code
        )
            .then((response) => response.json())
            .then((data) => {
                console.log(data)
                setResult(data)
                setLoading(false)
            })
            .catch((err) => {
                console.error(err)
                setLoading(true)
            });


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
                    {/* {loading && (
                        <div className="loader"></div>
                    )} */}

                </div>
                {result && (
                    <div className="vocabResultBox">
                        <div className="vocabResultRow">
                            <span className="vocabLabel">Translation:</span>
                            <span className={`vocabValue${loading ? " loading-blur" : ""}`}>
                                {loading ? "Loading..." : result?.translation ?? "-"}
                            </span>
                        </div>
                        <div className="vocabResultRow">
                            <span className="vocabLabel">Meaning:</span>
                            <span className={`vocabValue${loading ? " loading-blur" : ""}`}>
                                {loading ? "Loading meaning..." : result?.meaning ?? "-"}
                            </span>
                        </div>
                        <div className="vocabResultRow">
                            <span className="vocabLabel">Type:</span>
                            <span className={`vocabValue${loading ? " loading-blur" : ""}`}>
                                {loading ? "Loading..." : result?.type ?? "-"}
                            </span>
                        </div>
                        <div className="vocabResultRow">
                            <span className="vocabLabel">Synonyms:</span>
                            <span className={`vocabValue${loading ? " loading-blur" : ""}`}>
                                {loading ? "Loading, loading, loading" : result?.synonyms?.join(', ') ?? "-"}
                            </span>
                        </div>
                        <div className="vocabResultRow">
                            <span className="vocabLabel">Examples:</span>
                            <ul className="vocabExamples">
                                {(loading
                                    ? ["Loading example...", "Loading example...", "Loading example..."]
                                    : result?.examples ?? ["-", "-", "-"]
                                ).map((ex, idx) => (
                                    <li key={idx}>
                                        <span className={loading ? "loading-blur" : ""}>{ex}</span>
                                    </li>
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