import ReactCountryFlag from "react-country-flag";
import { languages } from "./languages";
import type { Country } from "../types/Country";

type LanguageSelectProps = {
    label: string;
    value: Country | null;
    onChange: (country: Country) => void;
};

const LanguageSelect: React.FC<LanguageSelectProps> = ({ label, value, onChange }) => {
    return (
        <div style={{ 'display': 'flex', 'flexDirection': 'column', 'gap': '1rem' }}>
            <label>
                {label}
                <select
                    value={value?.code || ""}
                    className="language-select"
                    onChange={e => {
                        const selected = languages.find(lg => lg.code == e.target.value);
                        if (selected) onChange(selected);
                    }}
                >
                    <option className="option-placeholder" value="">-- select language --</option>
                    {languages.map(lg => (
                        <option key={lg.name} value={lg.code}>
                            {lg.name}
                        </option>
                    ))}
                </select>
            </label>
            {value && (
                <span style={{ 'display': 'flex', 'justifyContent': 'center' }}>
                    <ReactCountryFlag
                        countryCode={value.country}
                        svg
                        style={{ width: "2em", height: "2em" }}
                    />
                </span>
            )}
        </div>
    )
}

export default LanguageSelect;