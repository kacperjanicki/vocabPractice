import { useState } from "react";
import LanguageSelect from "./LanguageSelect";

const ChooseLang = () => {
    type Country = {
        name: string;
        code: string;
    }

    const [nativeLanguage, setNativeLanguage] = useState<Country | null>(null);
    const [foreignLanguage, setForeignLanguage] = useState<Country | null>(null);

    // console.log("current setup: " + nativeLanguage);


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