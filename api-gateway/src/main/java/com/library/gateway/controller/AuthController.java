package com.library.gateway.controller;

import com.library.gateway.config.JwtUtil;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;
import reactor.core.publisher.Mono;

import java.util.Map;

@RestController
@RequestMapping("/api/auth")
public class AuthController {

    private final JwtUtil jwtUtil;

    public AuthController(JwtUtil jwtUtil) {
        this.jwtUtil = jwtUtil;
    }

    @PostMapping("/token")
    public Mono<Map<String, String>> generateToken(@RequestBody Map<String, String> request) {
        String username = request.getOrDefault("username", "anonymous");
        String token = jwtUtil.generateToken(username);
        return Mono.just(Map.of(
                "token", token,
                "type", "Bearer",
                "username", username
        ));
    }
}
