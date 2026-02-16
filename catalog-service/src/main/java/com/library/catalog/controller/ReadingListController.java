package com.library.catalog.controller;

import com.library.catalog.dto.AddBookRequest;
import com.library.catalog.dto.ReadingListCreateRequest;
import com.library.catalog.dto.ReadingListDTO;
import com.library.catalog.service.ReadingListService;
import jakarta.validation.Valid;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/reading-lists")
public class ReadingListController {

    private final ReadingListService readingListService;

    public ReadingListController(ReadingListService readingListService) {
        this.readingListService = readingListService;
    }

    @PostMapping
    public ResponseEntity<ReadingListDTO> createReadingList(@Valid @RequestBody ReadingListCreateRequest request) {
        ReadingListDTO created = readingListService.createReadingList(request);
        return ResponseEntity.status(HttpStatus.CREATED).body(created);
    }

    @GetMapping("/{id}")
    public ResponseEntity<ReadingListDTO> getReadingList(@PathVariable Long id) {
        return ResponseEntity.ok(readingListService.getReadingListById(id));
    }

    @GetMapping
    public ResponseEntity<List<ReadingListDTO>> getReadingListsByOwner(@RequestParam String ownerName) {
        return ResponseEntity.ok(readingListService.getReadingListsByOwner(ownerName));
    }

    @PostMapping("/{id}/books")
    public ResponseEntity<ReadingListDTO> addBookToReadingList(
            @PathVariable Long id,
            @Valid @RequestBody AddBookRequest request) {
        ReadingListDTO updated = readingListService.addBookToReadingList(id, request);
        return ResponseEntity.ok(updated);
    }

    @DeleteMapping("/{id}")
    public ResponseEntity<Void> deleteReadingList(@PathVariable Long id) {
        readingListService.deleteReadingList(id);
        return ResponseEntity.noContent().build();
    }
}
