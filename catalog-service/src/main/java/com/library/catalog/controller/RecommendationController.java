package com.library.catalog.controller;

import com.library.catalog.dto.RecommendationCreateRequest;
import com.library.catalog.dto.RecommendationDTO;
import com.library.catalog.service.RecommendationService;
import jakarta.validation.Valid;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api/recommendations")
public class RecommendationController {

    private final RecommendationService recommendationService;

    public RecommendationController(RecommendationService recommendationService) {
        this.recommendationService = recommendationService;
    }

    @PostMapping
    public ResponseEntity<RecommendationDTO> createRecommendation(
            @Valid @RequestBody RecommendationCreateRequest request) {
        RecommendationDTO created = recommendationService.createRecommendation(request);
        return ResponseEntity.status(HttpStatus.CREATED).body(created);
    }

    @GetMapping
    public ResponseEntity<Page<RecommendationDTO>> getAllRecommendations(Pageable pageable) {
        return ResponseEntity.ok(recommendationService.getAllRecommendations(pageable));
    }

    @GetMapping("/book/{bookId}")
    public ResponseEntity<Page<RecommendationDTO>> getRecommendationsByBook(
            @PathVariable Long bookId, Pageable pageable) {
        return ResponseEntity.ok(recommendationService.getRecommendationsByBook(bookId, pageable));
    }

    @DeleteMapping("/{id}")
    public ResponseEntity<Void> deleteRecommendation(@PathVariable Long id) {
        recommendationService.deleteRecommendation(id);
        return ResponseEntity.noContent().build();
    }
}
