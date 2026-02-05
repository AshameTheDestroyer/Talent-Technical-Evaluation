import { Button } from "./ui/button";
import { usePagination } from "~/hooks/use-pagination";
import { Combobox, ComboboxContent, ComboboxEmpty, ComboboxInput, ComboboxItem, ComboboxList } from "./ui/combobox";

export function Paginator({ total }: { total: number }) {
    const { page, limit, setPage, setLimit } = usePagination();
    const totalPages = Math.max(1, Math.ceil(total / Math.max(1, limit)));
    return (
        <footer className="flex place-items-center place-content-between gap-4 flex-wrap col-span-full">
            <div className="flex flex-wrap gap-4 place-items-center">
                <Button onClick={() => setPage(Math.max(1, page - 1))} disabled={page <= 1}>
                    Prev
                </Button>
                <span>Page {page} of {totalPages}</span>
                <Button onClick={() => setPage(Math.min(totalPages, page + 1))} disabled={page >= totalPages}>
                    Next
                </Button>
            </div>
            <div className="flex place-items-center gap-4">
                <p>Per page:</p>
                <Combobox items={[10, 25, 50, 100]} value={limit} onValueChange={(value) => { setLimit(value || 10); setPage(1); }}>
                    <ComboboxInput placeholder="Choose value" />
                    <ComboboxContent>
                        <ComboboxEmpty>No items found.</ComboboxEmpty>
                        <ComboboxList>
                            {(item) => (
                                <ComboboxItem key={item} value={item}>
                                    {item}
                                </ComboboxItem>
                            )}
                        </ComboboxList>
                    </ComboboxContent>
                </Combobox>
            </div>
        </footer>
    )
}