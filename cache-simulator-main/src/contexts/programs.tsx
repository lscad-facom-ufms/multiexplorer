import {createContext, FC, PropsWithChildren, useContext, useState} from "react";
import {PROGRAMS} from "../constants/programs.ts";

type Program = string[];
type Programs = Record<string, Program>;

export type ProgramContextType = {
    programs: Programs;
    setPrograms: (programs: Programs) => void;
}

export const ProgramContext = createContext<ProgramContextType>({} as ProgramContextType);
export const usePrograms = () => useContext(ProgramContext);

export const ProgramsProvider: FC<PropsWithChildren> = ({children}) => {
    // TODO persist to local storage
    const [programs, setPrograms] = useState<Programs>(PROGRAMS);

    const _setPrograms = (programs: Programs) => {
        setPrograms(programs);
    };

    return <ProgramContext.Provider value={{programs, setPrograms: _setPrograms}}>
        {children}
    </ProgramContext.Provider>
};
