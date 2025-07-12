import ReactCountryFlag from "react-country-flag";
import { countries } from "./countries";

type Country = {
    name: string;
    code: string;
}

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
                    onChange={e => {
                        const selected = countries.find(c => c.code == e.target.value);
                        if (selected) onChange(selected);
                    }}
                    style={{ marginLeft: 8 }}
                >
                    <option value="">-- select country --</option>
                    {countries.map(country => (
                        <option key={country.name} value={country.code}>
                            {country.name}
                        </option>
                    ))}
                </select>
            </label>
            {value && (
                <span style={{ 'display': 'flex', 'justifyContent': 'center' }}>
                    <ReactCountryFlag
                        countryCode={value.code}
                        svg
                        style={{ width: "2em", height: "2em" }}
                    />
                </span>
            )}
        </div>
    )
}

export default LanguageSelect;