import { useEffect } from "react";
import { useSearchParams } from "react-router";

export function usePagination() {
    const [searchParams, setSearchParams] = useSearchParams();
    const page = parseInt(searchParams.get("page") || "1", 10);
    const limit = parseInt(searchParams.get("limit") || "10", 10);

    // useEffect(() => {
    //     if (limit <= 0) {
    //         setLimit(10);
    //     }
    // }, [limit])

    function setPage(newPage: number) {
        searchParams.set("page", newPage.toString());
        setSearchParams(searchParams);
    }

    function setLimit(newLimit: number) {
        searchParams.set("limit", newLimit.toString());
        setSearchParams(searchParams);
    }

    return {
        page,
        limit,
        setPage,
        setLimit,
    };
}