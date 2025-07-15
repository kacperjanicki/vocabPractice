import { useState } from 'react'
import './index.css'
import { TbVocabulary } from "react-icons/tb";
import { RiAccountCircleFill } from "react-icons/ri";


import VocabEntry from './components/VocabEntry';
import ChooseLang from './components/ChooseLang';
import type { Country } from './types/Country';

const App: React.FC = () => {

  const [nativeLanguage, setNativeLanguage] = useState<Country | null>(null);
  const [foreignLanguage, setForeignLanguage] = useState<Country | null>(null);

  return (
    <div className='main-content'>
      <div className="header-bar" style={{
        display: 'flex',
        justifyContent: 'space-between',
        alignItems: 'center',
        padding: '0 1rem'
      }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '1rem' }}>
          <TbVocabulary size="70px" />
          <h1>VocabPractice</h1>
        </div>
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', cursor: 'pointer' }}>
          <span>Account</span>
          <RiAccountCircleFill size={24} />
        </div>
      </div>



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
    </div>
  )
}

export default App
