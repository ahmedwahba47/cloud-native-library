package com.library.catalog.service;

import com.library.catalog.client.LibraryApiClient;
import com.library.catalog.dto.*;
import com.library.catalog.entity.ReadingList;
import com.library.catalog.entity.ReadingListItem;
import com.library.catalog.repository.ReadingListRepository;
import io.github.resilience4j.circuitbreaker.annotation.CircuitBreaker;
import io.github.resilience4j.retry.annotation.Retry;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.time.LocalDate;
import java.util.List;

@Service
public class ReadingListService {

    private static final Logger log = LoggerFactory.getLogger(ReadingListService.class);

    private final ReadingListRepository readingListRepository;
    private final LibraryApiClient libraryApiClient;

    public ReadingListService(ReadingListRepository readingListRepository,
                              LibraryApiClient libraryApiClient) {
        this.readingListRepository = readingListRepository;
        this.libraryApiClient = libraryApiClient;
    }

    @Transactional
    public ReadingListDTO createReadingList(ReadingListCreateRequest request) {
        ReadingList readingList = ReadingList.builder()
                .name(request.getName())
                .description(request.getDescription())
                .ownerName(request.getOwnerName())
                .createdDate(LocalDate.now())
                .build();
        readingList = readingListRepository.save(readingList);
        return toDTO(readingList);
    }

    public List<ReadingListDTO> getReadingListsByOwner(String ownerName) {
        return readingListRepository.findByOwnerName(ownerName).stream()
                .map(this::toDTO)
                .toList();
    }

    public ReadingListDTO getReadingListById(Long id) {
        ReadingList readingList = readingListRepository.findById(id)
                .orElseThrow(() -> new RuntimeException("Reading list not found with id: " + id));
        return toDTO(readingList);
    }

    @Transactional
    @CircuitBreaker(name = "libraryApi", fallbackMethod = "addBookFallback")
    @Retry(name = "libraryApi")
    public ReadingListDTO addBookToReadingList(Long readingListId, AddBookRequest request) {
        ReadingList readingList = readingListRepository.findById(readingListId)
                .orElseThrow(() -> new RuntimeException("Reading list not found with id: " + readingListId));

        // Verify book exists in Library API (Service B)
        BookDTO book = libraryApiClient.getBookById(request.getBookId());
        log.info("Verified book exists: {} by {}", book.getTitle(), book.getAuthor());

        ReadingListItem item = ReadingListItem.builder()
                .bookId(request.getBookId())
                .addedDate(LocalDate.now())
                .notes(request.getNotes())
                .readingList(readingList)
                .build();
        readingList.getItems().add(item);
        readingList = readingListRepository.save(readingList);
        return toDTO(readingList);
    }

    @Transactional
    public ReadingListDTO addBookFallback(Long readingListId, AddBookRequest request, Throwable t) {
        log.warn("Circuit breaker fallback: Library API unavailable. Error: {}", t.getMessage());
        ReadingList readingList = readingListRepository.findById(readingListId)
                .orElseThrow(() -> new RuntimeException("Reading list not found with id: " + readingListId));

        // Add without verification
        ReadingListItem item = ReadingListItem.builder()
                .bookId(request.getBookId())
                .addedDate(LocalDate.now())
                .notes(request.getNotes() != null ? request.getNotes() + " [unverified]" : "[unverified - library service unavailable]")
                .readingList(readingList)
                .build();
        readingList.getItems().add(item);
        readingList = readingListRepository.save(readingList);
        return toDTO(readingList);
    }

    @Transactional
    public void deleteReadingList(Long id) {
        if (!readingListRepository.existsById(id)) {
            throw new RuntimeException("Reading list not found with id: " + id);
        }
        readingListRepository.deleteById(id);
    }

    private ReadingListDTO toDTO(ReadingList readingList) {
        List<ReadingListItemDTO> itemDTOs = readingList.getItems().stream()
                .map(this::toItemDTO)
                .toList();

        return ReadingListDTO.builder()
                .id(readingList.getId())
                .name(readingList.getName())
                .description(readingList.getDescription())
                .ownerName(readingList.getOwnerName())
                .createdDate(readingList.getCreatedDate())
                .items(itemDTOs)
                .build();
    }

    private ReadingListItemDTO toItemDTO(ReadingListItem item) {
        try {
            BookDTO book = libraryApiClient.getBookById(item.getBookId());
            return ReadingListItemDTO.builder()
                    .id(item.getId())
                    .bookId(item.getBookId())
                    .bookTitle(book.getTitle())
                    .bookAuthor(book.getAuthor())
                    .addedDate(item.getAddedDate())
                    .notes(item.getNotes())
                    .readStatus(item.getReadStatus().name())
                    .build();
        } catch (Exception e) {
            log.warn("Library API unavailable for book enrichment: {}", e.getMessage());
            return ReadingListItemDTO.builder()
                    .id(item.getId())
                    .bookId(item.getBookId())
                    .bookTitle("Unavailable")
                    .bookAuthor("Unavailable")
                    .addedDate(item.getAddedDate())
                    .notes(item.getNotes())
                    .readStatus(item.getReadStatus().name())
                    .build();
        }
    }
}
