import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import org.json.*;

public class VogueImageScraper {
    private static final String ENDPOINT = "https://graphql.condenast.io/graphql";

    public static void main(String[] args) throws Exception {
        String brandSlug = "issey-miyake";

        String query = """
        query BrandShows($brandSlug: String!) {
          brand(slug: $brandSlug) {
            slug
            name
            shows {
              slug
              season
              year
              looks {
                slug
                photos {
                  url
                }
              }
            }
          }
        }
        """;

        JSONObject jsonBody = new JSONObject()
            .put("query", query)
            .put("variables", new JSONObject().put("brandSlug", brandSlug));

        HttpClient client = HttpClient.newHttpClient();
        HttpRequest request = HttpRequest.newBuilder()
            .uri(URI.create(ENDPOINT))
            .header("Content-Type", "application/json")
            .header("User-Agent", "Mozilla/5.0")
            .POST(HttpRequest.BodyPublishers.ofString(jsonBody.toString()))
            .build();

        HttpResponse<String> resp = client.send(request, HttpResponse.BodyHandlers.ofString());
        JSONObject respJson = new JSONObject(resp.body());

        System.out.println(respJson.toString(2));

        // Now traverse respJson to extract each photo URL
        JSONObject brand = respJson.getJSONObject("data").getJSONObject("brand");
        JSONArray shows = brand.getJSONArray("shows");

        for (int i = 0; i < shows.length(); i++) {
            JSONObject show = shows.getJSONObject(i);
            String showSlug = show.getString("slug");
            JSONArray looks = show.getJSONArray("looks");
            for (int j = 0; j < looks.length(); j++) {
                JSONObject look = looks.getJSONObject(j);
                JSONArray photos = look.getJSONArray("photos");
                for (int k = 0; k < photos.length(); k++) {
                    String imgUrl = photos.getJSONObject(k).getString("url");
                    System.out.println("Show: " + showSlug + " Look: " + j + " URL: " + imgUrl);
                }
            }
        }
    }
}


