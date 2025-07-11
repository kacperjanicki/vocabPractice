import { useState } from 'react';
import '../index.css'
import { CiSquarePlus } from "react-icons/ci";

const VocabEntry = () => {

    const [word, setWord] = useState("");

    const submitWord = () => {
        console.log(word);
    }

    return (
        <div className="vocabEntry">
            <input
                type="text"
                placeholder="Your word..."
                className="w-full max-w-md px-4 py-2 rounded-xl bg-zinc-800 text-zinc-100 placeholder-zinc-500 border border-zinc-700 focus:outline-none focus:ring-2 focus:ring-indigo-500 transition duration-200 font-mono text-base shadow-md"
                onChange={(e) => setWord(e.target.value)}
                onKeyDown={(e) => e.key == 'Enter' ? submitWord() : ''}
            />
            <CiSquarePlus size="25px" className="btnIcon" onClick={submitWord} />
        </div>
    )
}

export default VocabEntry;