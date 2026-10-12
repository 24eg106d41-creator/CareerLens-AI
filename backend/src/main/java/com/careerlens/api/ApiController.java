package com.careerlens.api;
import java.util.*;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.http.*;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.client.RestClient;
import jakarta.validation.Valid;
import jakarta.validation.constraints.NotBlank;

@RestController @RequestMapping("/api")
public class ApiController {
 private final RestClient client;
 public ApiController(@Value("${careerlens.ai.url:http://localhost:8001}") String aiUrl){client=RestClient.builder().baseUrl(aiUrl).build();}
 public record AnalyzeRequest(@NotBlank String resume_text,@NotBlank String job_description){}
 public record AuthRequest(@NotBlank String email,@NotBlank String password){}
 @GetMapping("/health") public Map<String,String> health(){return Map.of("status","ok");}
 @PostMapping("/career/analyze") public Map<?,?> analyze(@Valid @RequestBody AnalyzeRequest req){return client.post().uri("/analyze").contentType(MediaType.APPLICATION_JSON).body(req).retrieve().body(Map.class);}
 @PostMapping("/resume/upload") public ResponseEntity<Map<String,String>> uploadInfo(){return ResponseEntity.status(HttpStatus.NOT_IMPLEMENTED).body(Map.of("message","Upload PDF directly to AI service at /resume/extract; frontend demo uses that endpoint."));}
 @PostMapping("/auth/register") public ResponseEntity<Map<String,String>> register(@Valid @RequestBody AuthRequest req){return ResponseEntity.status(501).body(Map.of("message","Demo authentication is not configured. Configure database-backed users and JWT signing before exposing this service."));}
 @PostMapping("/auth/login") public ResponseEntity<Map<String,String>> login(@Valid @RequestBody AuthRequest req){return ResponseEntity.status(501).body(Map.of("message","Demo authentication is not configured. Configure database-backed users and JWT signing before exposing this service."));}
 @GetMapping("/career/roadmap/{userId}") public ResponseEntity<Map<String,String>> roadmap(@PathVariable String userId){return ResponseEntity.status(501).body(Map.of("message","Persist analysis results before enabling user history."));}
 @GetMapping("/career/projects/{userId}") public ResponseEntity<Map<String,String>> projects(@PathVariable String userId){return ResponseEntity.status(501).body(Map.of("message","Persist analysis results before enabling user history."));}
 @GetMapping("/career/interview/{userId}") public ResponseEntity<Map<String,String>> interview(@PathVariable String userId){return ResponseEntity.status(501).body(Map.of("message","Persist analysis results before enabling user history."));}
}
