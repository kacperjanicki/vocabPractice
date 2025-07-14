import { useState } from 'react'
import './index.css'
import { TbVocabulary } from "react-icons/tb";

import VocabEntry from './components/VocabEntry';
import ChooseLang from './components/ChooseLang';

const App: React.FC = () => {
  console.clear();
  const [count, setCount] = useState(0)

  let hobbies: string[] = [];
  hobbies.push("a");

  const printStudent = (stud: Student) => {
    // let s = ""
    // for (const i in stud) {
    //   s += i + '\n';
    // }
    // console.log(s);
    console.log(Object.keys(stud).join('\n'));
  }

  interface Person {
    name: string;
    age: number;
    hobbies?: string[];
  }
  interface Student extends Person {
    indexNumber: number;
    degree: string;
  }

  let stud1: Student = {
    name: "jack",
    age: 21,
    hobbies: ["swimming", "triathlon"],
    indexNumber: 2134,
    degree: "CS"
  }
  // printStudent(stud1);

  // let p1: Person = {
  //   name: "kacper",
  //   age: 10,
  // }

  // let printPerson = (per: Person) => { console.log(per) };

  // printPerson(p1);

  // printPerson = () => { console.log("a") };

  return (
    <div className='main-content'>
      <div style={{ 'display': 'flex', justifyContent: 'center', gap: '1rem' }}>
        <TbVocabulary size="70px" />
        <h1> VocabPractice</h1>
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




      <ChooseLang />

      <VocabEntry />
    </div>
  )
}

export default App
