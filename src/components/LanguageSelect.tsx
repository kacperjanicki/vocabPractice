import { countries } from "./countries";
import ReactCountryFlag from "react-country-flag";


type LanguageSelectProps = {
    label: string;
    value: string;
    onChange: (code: string) => void;
};

const LanguageSelect: React.FC<LanguageSelectProps> = ({ label, value, onChange }) => {
    return (
        <div style={{ marginBottom: "1em" }}>
            <label>
                {label}
                <select
                    value={value}
                    onChange={e => onChange(e.target.value)}
                    style={{ marginLeft: 8 }}
                >
                    <option value="">-- wybierz kraj --</option>
                    {countries.map(country => (
                        <option key={country.code} value={country.code}>
                            {country.name}
                        </option>
                    ))}
                </select>
            </label>
            {value && (
                <span style={{ marginLeft: 10 }}>
                    <ReactCountryFlag
                        countryCode={value}
                        svg
                        style={{ width: "2em", height: "2em" }}
                    />
                </span>
            )}
        </div>
    )
}

export default LanguageSelect;