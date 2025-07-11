import React, { useState } from "react";
import ReactCountryFlag from "react-country-flag"
import { countries } from "./countries";
import LanguageSelect from "./LanguageSelect";




const ChooseLang = () => {
    const [nativeLanguage, setNativeLanguage] = useState("");
    const [foreignLanguage, setForeignLanguage] = useState("")


    const handleChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
        setNativeLanguage(e.target.value)
        console.log(nativeLanguage);
    }

    return (
        <div>
            <LanguageSelect
                label="Native Language"
                value={nativeLanguage}
                onChange={setNativeLanguage}
            />

            <LanguageSelect
                label="Foreign Language"
                value={foreignLanguage}
                onChange={setForeignLanguage}
            />


        </div>

    )
}

export default ChooseLang;