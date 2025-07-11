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
    <>
      <TbVocabulary size="70px" />
      <h1> VocabPractice</h1>

      <ChooseLang />

      <VocabEntry />
    </>
  )
}

export default App
