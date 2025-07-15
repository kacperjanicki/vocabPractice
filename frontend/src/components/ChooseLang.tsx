import { useEffect } from "react";
import LanguageSelect from "./LanguageSelect";
import type { Country } from "../types/Country";
import { languages } from "./languages";

type ChooseLangProps = {
    nativeLanguage: Country | null;
    setNativeLanguage: (lang: Country | null) => void;
    foreignLanguage: Country | null;
    setForeignLanguage: (lang: Country | null) => void;
};

const ChooseLang = ({
    nativeLanguage,
    setNativeLanguage,
    foreignLanguage,
    setForeignLanguage
}: ChooseLangProps) => {


    const defaultNative = languages.find(lang => lang.code === "pl");
    const defaultForeign = languages.find(lang => lang.code === "en");

    useEffect(() => {
        if (!nativeLanguage && defaultNative) {
            setNativeLanguage(defaultNative);
        }
        if (!foreignLanguage && defaultForeign) {
            setForeignLanguage(defaultForeign);
        }
    }, []);

    return (
        <div className="langSelectContainer">
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