package com.library.catalog.service;

import com.library.catalog.client.LibraryApiClient;
import com.library.catalog.dto.*;
import com.library.catalog.entity.Recommendation;
import com.library.catalog.repository.RecommendationRepository;
import io.github.resilience4j.circuitbreaker.annotation.CircuitBreaker;
import io.github.resilience4j.retry.annotation.Retry;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.time.LocalDate;

@Service
public class RecommendationService {

    private static final Logger log = LoggerFactory.getLogger(RecommendationService.class);

    private final RecommendationRepository recommendationRepository;
    private final LibraryApiClient libraryApiClient;

    public RecommendationService(RecommendationRepository recommendationRepository,
                                  LibraryApiClient libraryApiClient) {
        this.recommendationRepository = recommendationRepository;
        this.libraryApiClient = libraryApiClient;
    }

    @Transactional
    @CircuitBreaker(name = "libraryApi", fallbackMethod = "createRecommendationFallback")
    @Retry(name = "libraryApi")
    public RecommendationDTO createRecommendation(RecommendationCreateRequest request) {
        // Verify book exists
        BookDTO book = libraryApiClient.getBookById(request.getBookId());
        log.info("Creating recommendation for book: {}", book.getTitle());

        Recommendation recommendation = Recommendation.builder()
                .bookId(request.getBookId())
                .recommendedBy(request.getRecommendedBy())
                .reason(request.getReason())
                .rating(request.getRating())
                .createdDate(LocalDate.now())
                .build();
        recommendation = recommendationRepository.save(recommendation);
        return toDTO(recommendation, book);
    }

    public RecommendationDTO createRecommendationFallback(RecommendationCreateRequest request, Throwable t) {
        log.warn("Fallback: Creating recommendation without book verification. Error: {}", t.getMessage());
        Recommendation recommendation = Recommendation.builder()
                .bookId(request.getBookId())
                .recommendedBy(request.getRecommendedBy())
                .reason(request.getReason())
                .rating(request.getRating())
                .createdDate(LocalDate.now())
                .build();
        recommendation = recommendationRepository.save(recommendation);
        return toDTO(recommendation, null);
    }

    public Page<RecommendationDTO> getRecommendationsByBook(Long bookId, Pageable pageable) {
        return recommendationRepository.findByBookId(bookId, pageable)
                .map(this::toDTOWithBookLookup);
    }

    public Page<RecommendationDTO> getAllRecommendations(Pageable pageable) {
        return recommendationRepository.findAll(pageable)
                .map(this::toDTOWithBookLookup);
    }

    @Transactional
    public void deleteRecommendation(Long id) {
        if (!recommendationRepository.existsById(id)) {
            throw new RuntimeException("Recommendation not found with id: " + id);
        }
        recommendationRepository.deleteById(id);
    }

    private RecommendationDTO toDTOWithBookLookup(Recommendation recommendation) {
        try {
            BookDTO book = libraryApiClient.getBookById(recommendation.getBookId());
            return toDTO(recommendation, book);
        } catch (Exception e) {
            return toDTO(recommendation, null);
        }
    }

    private RecommendationDTO toDTO(Recommendation recommendation, BookDTO book) {
        return RecommendationDTO.builder()
                .id(recommendation.getId())
                .bookId(recommendation.getBookId())
                .bookTitle(book != null ? book.getTitle() : "Unavailable")
                .bookAuthor(book != null ? book.getAuthor() : "Unavailable")
                .recommendedBy(recommendation.getRecommendedBy())
                .reason(recommendation.getReason())
                .rating(recommendation.getRating())
                .createdDate(recommendation.getCreatedDate())
                .build();
    }
}
