import { useState } from 'react'
import './index.css'
import { TbVocabulary } from "react-icons/tb";
import { RiAccountCircleFill } from "react-icons/ri";
import { useNavigate, Routes, Route } from 'react-router-dom';


import VocabEntry from './components/VocabEntry';
import ChooseLang from './components/ChooseLang';
import type { Country } from './types/Country';

const App: React.FC = () => {
  const navigate = useNavigate();

  const [nativeLanguage, setNativeLanguage] = useState<Country | null>(null);
  const [foreignLanguage, setForeignLanguage] = useState<Country | null>(null);

  const changeLocation = (location: string) => () => {
    navigate(location);
  };

  return (
    <>
      <div className="header-bar">
        <div className="header-item clickable" onClick={changeLocation("/")}>
          <TbVocabulary size={56} />
          <span className="header-label">VocabPractice</span>
        </div>

        <div className="header-item clickable" onClick={changeLocation("/me")}>
          <RiAccountCircleFill size={56} />
          <span className="header-label">Account</span>
        </div>

      </div>

      <div className='main-content'>
        <Routes>
          <Route path="/" element={
            <>
              <div className='description'>
                <p>Generating quotes, synonyms and meanings for your words is done with self-hosted AI model</p>
                <p>I made this tool to help me learn English vocabulary better, here in one place you have everything: meaning, synonyms, sentence examples and pronunciation.</p>

                <p>If you have an .epub file, you can upload it to get sentence examples — you will receive quotes taken directly from the book you are learning from.
                  We only use your file to search for sentences that include the word you entered. The file is not stored or saved after scanning.
                </p>

                <p>After adding a word, to have all data visible, you might have to wait up to 15 seconds
                  While you're waiting, simple meaning and translation will be given to you, thanks to <a href="https://libretranslate.com/" style={{ color: '#63B0CD' }} target="_blank"
                    rel="noopener noreferrer">LibreTranslate</a>
                </p>
              </div>

              <ChooseLang
                nativeLanguage={nativeLanguage}
                setNativeLanguage={setNativeLanguage}
                foreignLanguage={foreignLanguage}
                setForeignLanguage={setForeignLanguage}
              />
              <VocabEntry
                nativeLanguage={nativeLanguage}
                foreignLanguage={foreignLanguage}
              />
            </>
          } />
          <Route path="/me" element={<h1>User profile</h1>} />

        </Routes >
      </div>
    </>
  )
}

export default App
