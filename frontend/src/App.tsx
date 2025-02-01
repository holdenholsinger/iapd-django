import { useState } from "react";
import "./App.css";
import Form from "./Form";

function App() {
    // when I get on next, I need to figure out how to pass the form data to the endpoint
    const [firmInfo, setFirmInfo] = useState(null);
    const [errorMessage, setErrorMessage] = useState<string | null>(null);

    const handleFormSubmit = (crdNumber: string) => {
        fetch(`http://localhost:8000/api/iapd-info/${crdNumber}`)
            .then((response) => {
                if (!response.ok) {
                    throw new Error("Unable to fetch data");
                } else {
                    return response.json();
                }
            })
            .then((responseJson) => setFirmInfo(responseJson))
            .then(() => setErrorMessage(null))
            .catch(() => {
                setErrorMessage("Please enter a valid CRD number");
                setFirmInfo(null);
            });
    };

    return (
        <>
            <h1 className="mb-4 text-4xl font-extrabold leading-none tracking-tight text-gray-900 md:text-5xl lg:text-6xl dark:text-white pl-3 pb-3 bg-blue-400">
                ADV Information Finder
            </h1>
            <div className="pl-3">
                <Form onSubmit={handleFormSubmit}></Form>
                <br />
                {firmInfo && (
                    <>
                        <table className="border-spacing-y-2">
                            <tbody>
                                <tr>
                                    <td className="py-2 w-40 font-bold">
                                        Firm name:
                                    </td>
                                    <td className="px-4">
                                        {firmInfo.firm_name}
                                    </td>
                                </tr>
                                <tr className="border-t-2">
                                    <td className="py-2 w-40 font-bold">
                                        Address 1:
                                    </td>
                                    <td className="px-4">
                                        {firmInfo.address1}
                                    </td>
                                </tr>
                                {firmInfo.address2 && (
                                    <tr>
                                        <td className="py-2 w-40 font-bold">
                                            Address 2:
                                        </td>
                                        <td className="px-4">
                                            {firmInfo.address2}
                                        </td>
                                    </tr>
                                )}
                                <tr>
                                    <td className="py-2 w-40 font-bold">
                                        City:
                                    </td>
                                    <td className="px-4">{firmInfo.city}</td>
                                </tr>
                                <tr>
                                    <td className="py-2 w-40 font-bold">
                                        State:
                                    </td>
                                    <td className="px-4">{firmInfo.state}</td>
                                </tr>
                                <tr>
                                    <td className="py-2 w-40 font-bold">
                                        Zip:
                                    </td>
                                    <td className="px-4">{firmInfo.zip}</td>
                                </tr>
                                <tr className="border-t-2">
                                    <td className="py-2 w-40 font-bold">
                                        Employee count:
                                    </td>
                                    <td className="px-4">
                                        {firmInfo.employee_count}
                                    </td>
                                </tr>
                                <tr className="border-t-2">
                                    <td className="py-2 w-40 font-bold">
                                        Number of employees providing advisory
                                        functions:
                                    </td>
                                    <td className="px-4">
                                        {firmInfo.advisory_employees}
                                    </td>
                                </tr>
                                <tr className="border-t-2">
                                    <td className="py-2 w-40 font-bold">
                                        AUM:
                                    </td>
                                    <td className="px-4">{firmInfo.aum}</td>
                                </tr>
                                <tr className="border-t-2">
                                    <td className="py-2 w-40 font-bold">
                                        Private fund count:
                                    </td>
                                    <td className="px-4">
                                        {firmInfo.private_funds_count}
                                    </td>
                                </tr>
                                <tr className="border-t-2">
                                    <td className="py-2 w-40 font-bold">
                                        Hedge funds count:
                                    </td>
                                    <td className="px-4">
                                        {firmInfo.hedge_fund_count}
                                    </td>
                                </tr>
                                <tr className="border-t-2">
                                    <td className="py-2 w-40 font-bold">
                                        Percent of assets in derivatives:
                                    </td>
                                    <td className="px-4">
                                        {firmInfo.percent_derivatives
                                            ? `${firmInfo.percent_derivatives}%`
                                            : "0%"}
                                    </td>
                                </tr>
                            </tbody>
                        </table>
                    </>
                )}
                {errorMessage && (
                    <div className="text-red-800 font-bold">{errorMessage}</div>
                )}
            </div>
        </>
    );
}

export default App;
