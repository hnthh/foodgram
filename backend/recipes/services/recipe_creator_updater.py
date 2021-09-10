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

    def _create_recipe_ingredients(self, recipe):
        from ingredients.models import RecipeIngredient

        ingredients = list()
        for item in self.ingredients:
            ingredient, amount = item.values()
            ingredients.append(
                RecipeIngredient(recipe=recipe, ingredient=ingredient, amount=amount),
            )

        RecipeIngredient.objects.bulk_create(ingredients)


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
        return Recipe.objects.get(id=pk)
