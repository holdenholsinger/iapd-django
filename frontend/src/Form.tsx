import { useState } from "react";

interface FormProps {
    onSubmit: (crdNumber: string) => void;
}
function Form({ onSubmit }: FormProps) {
    const [crdNumber, setCrdNumber] = useState("");

    const handleSubmit = (e: React.FormEvent) => {
        e.preventDefault();
        if (crdNumber) {
            onSubmit(crdNumber);
        }
    };

    return (
        <div className="max-w-sm ml-0">
            <form
                className="flex flex-col space-y-4 items-start"
                onSubmit={handleSubmit}
            >
                <label className="font-bold" htmlFor="crd">
                    CRD number:{" "}
                </label>
                <div className="flex flex-row ">
                    <input
                        className="w-1/4 rounded border"
                        id="crd"
                        type="text"
                        name="crd"
                        onChange={(e) => setCrdNumber(e.target.value)}
                        required
                    ></input>
                    <button
                        className="bg-blue-400 ml-1 p-1.5 rounded border hover:bg-blue-300 font-bold"
                        type="submit"
                    >
                        Submit
                    </button>
                </div>
            </form>
        </div>
    );
}

export default Form;
