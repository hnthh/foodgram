from ingredients.models import RecipeIngredient
from recipes.models import Recipe


class BaseService:
    def __init__(self, author, name, text, image, cooking_time, ingredients, tags):
        self.author = author
        self.name = name
        self.text = text
        self.image = image
        self.cooking_time = cooking_time
        self.ingredients = ingredients
        self.tags = tags

    def _set_tags(self, recipe):
        recipe.tags.set(self.tags)

    def _prepare_recipe_ingredients(self, recipe):
        out = list()
        for item in self.ingredients:
            ingredient, amount = item.values()
            out.append(
                RecipeIngredient(
                    recipe=recipe,
                    ingredient=ingredient,
                    amount=amount,
                ),
            )
        return out

    def _create_recipe_ingredients(self, recipe):
        RecipeIngredient.objects.bulk_create(
            self._prepare_recipe_ingredients(recipe),
        )


class RecipeCreator(BaseService):
    def __call__(self):
        recipe = self.create()

        self._create_recipe_ingredients(recipe)
        self._set_tags(recipe)

        return recipe

    def create(self):
        return Recipe.objects.create(
            author=self.author,
            name=self.name,
            text=self.text,
            image=self.image,
            cooking_time=self.cooking_time,
        )


class RecipeUpdater(BaseService):
    def __init__(self, recipe, author, name, text, image, cooking_time, ingredients, tags):
        super().__init__(author, name, text, image, cooking_time, ingredients, tags)

        self.recipe = recipe

    def __call__(self):
        self._remove_nested_objects()

        recipe = self.update()

        self._create_recipe_ingredients(recipe)
        self._set_tags(recipe)

        return recipe

    def _get_updated(self, id):
        return Recipe.objects.get(id=id)

    def _remove_nested_objects(self):
        self.recipe.recipeingredient_set.all().delete()
        self.recipe.tags.remove()

    def update(self):
        pk = Recipe.objects.filter(id=self.recipe.id).update(
            author=self.author,
            name=self.name,
            text=self.text,
            image=self.image,
            cooking_time=self.cooking_time,
        )
        return self._get_updated(pk)
